"""
    @public
"""
from __future__ import annotations
from dataclasses import dataclass, field as data_field
from types import SimpleNamespace
from .type_registry import TypeRegistry
from rx.core.typing import Scheduler
from .struct import StructRegistry
from anyio import create_task_group, Lock
from anyio.to_thread import run_sync
from .format import Format, get_preferred_file
from .format_registry import FormatRegistry
from .preprocess_struct import preprocess_struct_def
from .promise import Promise
from pathlib import Path
from public import public
from importlib.resources import open_text, contents
from functools import partial, wraps
from operator import attrgetter, methodcaller
from itertools import groupby
from more_itertools import take


def is_loadable(path, model):
    print(path)
    return path.suffix in model.formats.by_suffix


def async_cache(func):
    cache = {}

    @wraps(func)
    async def cache_func(*args):
        if args in cache:
            return await cache[args]

        future = func(*args)
        cache[args] = future
        try:
            return await future
        except Exception:
            del cache[args]
            raise

    return cache_func


@async_cache
async def get_contents(package, model: Model):
    resources = await run_sync(contents, package)

    resources = (
        Path(resource)
        for resource in resources
        if Path(resource).suffix in model.formats.by_suffix
    )

    return tuple(
        get_preferred_file(files, model)
        for name, files in groupby(resources, attrgetter('stem'))
    )


class AsyncIterator:
    def __init__(self, iterator, batch_size=10):
        self.iter = iter(iterator)
        self.batch_size = batch_size
        self.batch = []
        self.done = False

    def __aiter__(self):
        return self

    async def __anext__(self):
        if not self.batch and not self.done:
            await run_sync(
                self.__next,
                cancellable=True,
            )

        elif not self.batch and self.done:
            raise StopAsyncIteration()

        return self.batch.pop()

    def __next(self):
        self.batch = take(self.batch_size, self.iter)
        self.batch.reverse()
        if len(self.batch) != self.batch_size:
            self.done = True


@public
@dataclass
class Model:
    name: str
    types: SimpleNamespace = data_field(init=False, repr=False)
    structs: StructRegistry = data_field(init=False, repr=False)
    scheduler: Scheduler = None
    formats: FormatRegistry = data_field(init=False, repr=False)

    def __hash__(self):
        return hash(id(self))

    def __post_init__(self):
        self.types = TypeRegistry(self)
        self.structs = StructRegistry(self)
        self.formats = FormatRegistry(self)
        self.__loading_structs = {}
        self.__struct_locations = {}
        self.__struct_loading_lock = Lock()

    async def load_meta_struct(self, struct_name):
        if struct_name in self.structs:
            return self.structs[struct_name]

        struct_def = await self.load_struct_def_resource(
            Path(struct_name).with_suffix('.json'),
            'omniblack.model.structs',
        )

        child_fields = filter(
            lambda field: field['type'] == 'child',
            struct_def.fields,
        )

        async with create_task_group() as tg:
            for child_field in child_fields:
                tg.start_soon(
                    self.load_meta_struct,
                    child_field['attrs']['struct_name'],
                )

        return self.structs[struct_name]

    async def load_model_dir(self, dir: Path):
        async with create_task_group() as tg:
            dir_iter = filter(methodcaller('is_file'), dir.iterdir())
            dir_iter = filter(partial(is_loadable, model=self), dir_iter)
            sort_dir_iter = partial(sorted, dir_iter, key=attrgetter('stem'))
            dir_iter = await run_sync(sort_dir_iter)

            for name, paths in groupby(dir_iter, attrgetter('stem')):
                path = get_preferred_file(paths, self)
                tg.start_soon(self.load_struct_def_file, path)

    async def load_model_package(self, package):
        async with create_task_group() as tg:
            for resource in await get_contents(package, self):
                tg.start_soon(
                    self.load_struct_def_resource,
                    resource,
                    package,
                )

    async def load_struct_def_file(self, path):
        name = path.stem
        existing_prom = None
        promise = Promise()

        async with self.__struct_loading_lock:
            if name in self.__loading_structs:
                if self.__struct_locations[name] != path:
                    raise ValueError(
                        f'Conflicting paths found for {name}.'
                        ' Structs may not be loaded twice.',
                        path,
                        self.__struct_locations[name]
                    )

                existing_prom = self.__loading_structs[name]
            else:
                self.__loading_structs[name] = promise
                self.__struct_locations[name] = promise

        if existing_prom is not None:
            return await existing_prom

        try:
            format = self.formats.by_suffix[path.suffix]
            struct_def = await run_sync(
                self.load_file,
                path,
                format,
            )

            struct_cls = await self.__load_struct_def(struct_def)
        except Exception as err:
            promise.reject(err)
            raise

        promise.resolve(struct_cls)
        return struct_cls

    async def __load_struct_def(self, struct_def):
        meta_structs, = preprocess_struct_def(struct_def)
        async with create_task_group() as tg:
            for struct_name in meta_structs:
                tg.start_soon(
                    self.load_meta_struct,
                    struct_name,
                )

        return self.structs(struct_def)

    async def load_struct_def_resource(self, resource_path, package):
        struct_name = resource_path.name
        promise = Promise()
        existing_prom = None
        async with self.__struct_loading_lock:
            if struct_name in self.__loading_structs:
                if package != self.__struct_locations[struct_name]:
                    raise ValueError(
                        f'Conflicting paths found for {struct_name}.'
                        ' Structs may not be loaded twice.',
                        (resource_path, package),
                        self.__struct_locations[struct_name]
                    )

                existing_prom = self.__loading_structs[struct_name]
            else:
                self.__loading_structs[struct_name] = promise
                self.__struct_locations[struct_name] = resource_path

        if existing_prom is not None:
            return await existing_prom

        try:
            format = self.formats.by_suffix[resource_path.suffix]
            struct_def = await run_sync(
                self.load_resource,
                resource_path,
                package,
                format,
            )

            struct_cls = await self.__load_struct_def(struct_def)
            promise.resolve(struct_cls)
            return struct_cls
        except Exception as err:
            promise.reject(err)
            raise

    def load_resource(self, resource: Path, package: str, format: Format):
        with open_text(package, str(resource)) as file_obj:
            return format.load(file_obj)

    def load_file(self, path: Path, format: Format):
        with open(path) as file_obj:
            return format.load(file_obj)

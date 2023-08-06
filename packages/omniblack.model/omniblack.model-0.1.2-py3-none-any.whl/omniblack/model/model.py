"""
    @public
"""
from __future__ import annotations
from dataclasses import dataclass, field as data_field
from types import SimpleNamespace
from .type_registry import create_registry
from rx.core.typing import Scheduler
from .struct import StructRegistry, meta_model_path
from anyio import create_task_group
from anyio.to_thread import run_sync
from itertools import islice
from .abc import FormatRegistry, Format
from .preprocess_struct import preprocess_struct_def
from .promise import Promise
from pathlib import Path
from more_itertools import unique_everseen
from public import public


def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))


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

    def __post_init__(self):
        self.types = create_registry(self)
        self.structs = StructRegistry(self)
        self.formats = FormatRegistry()
        self.__loading_structs = {}
        self.__struct_paths = {}

    async def load_meta_struct(self, struct_name):
        if struct_name in self.structs:
            return self.structs[struct_name]

        struct_path = meta_model_path/struct_name

        struct_def = await self.load_struct_def(struct_path)
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

    async def load_model(self, dir: Path):
        async with create_task_group() as tg:
            dir_iter = unique_everseen(
                filter(lambda path: path.is_file(), dir.iterdir()),
                lambda path: path.stem,
            )

            async for path in AsyncIterator(dir_iter):
                if path.suffix in Format.formats_by_suffix:
                    tg.start_soon(self.load_struct_def, path.with_suffix(''))

    async def load_struct_def(self, path):
        name = path.stem
        if name in self.__loading_structs:
            if self.__struct_paths[name] != path:
                raise ValueError(
                    f'Conflicting paths found for {name}.'
                    ' Structs may not be loaded twice.',
                    path,
                    self.__struct_paths[name]
                )

            return await self.__loading_structs[name]
        promise = Promise()

        self.__loading_structs[name] = promise
        self.__struct_paths[name] = promise

        try:
            for format in self.formats.values():
                format_path = path.with_suffix(format.file_suffix)
                try:
                    struct_def = await run_sync(
                        self.load_file,
                        format_path,
                        format,
                    )
                except FileNotFoundError:
                    continue

                meta_structs, = preprocess_struct_def(struct_def)

                async with create_task_group() as tg:
                    for struct_name in meta_structs:
                        tg.start_soon(
                            self.load_meta_struct,
                            struct_name,
                        )

                struct_cls = self.structs(struct_def)
                break
            else:
                extensions = (
                    format.file_extension
                    for format in self.formats.values()
                )
                extension_str = ', '.join(extensions)
                raise FileNotFoundError(
                    f'No file found with correct extension at {path} .'
                    f' Available extensions are {extension_str}.'
                )
        except Exception as err:
            promise.reject(err)
            raise

        promise.resolve(struct_cls)
        return struct_cls

    def load_file(self, path, format: Format):
        with open(path) as file_obj:
            return format.load(file_obj)

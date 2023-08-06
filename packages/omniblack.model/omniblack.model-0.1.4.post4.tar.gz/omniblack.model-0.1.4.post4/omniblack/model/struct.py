from __future__ import annotations
from itertools import chain
from importlib import import_module
from pathlib import Path
from collections.abc import Mapping
from operator import getitem
from typing import TYPE_CHECKING, Union

from rx import combine_latest
from rx.operators import map
from anyio.to_thread import run_sync
from public import public
from importlib.resources import open_text
from json import load

from .field import Field, UiString
from .undefined import undefined
from .dot_path import DotPath
from .abc import Registry

if TYPE_CHECKING:
    from .model import Model

bases_path = DotPath(('implementation', 'python', 'bases'))

struct_def_file = open_text('omniblack.model.structs', 'struct.json')
# The struct def of struct
struct_struct_def = load(struct_def_file)


def is_ui_string(field):
    return (
        field['type'] == 'child'
        and field['attrs']['struct_name'] == 'ui_string'
    )


root_ui_string = {
    field['name']
    for field in struct_struct_def['fields']
    if is_ui_string(field)
}

struct_fields = tuple(field['name'] for field in struct_struct_def['fields'])


def import_base(base_str):
    module_id, name = base_str.split(':')
    module = import_module(module_id)
    return getattr(module, name)


class StructMeta(type):
    def __new__(
            cls,
            name,
            bases,
            attrs: dict,
            struct_def: dict,
            model: Model,
            is_base=False,
    ):
        model_bases = (
            import_base(base)
            for base in bases_path.get(struct_def, tuple())
        )
        final_bases = tuple(chain(model_bases, bases))

        fields = []
        if not is_base:
            attrs['_Struct__model'] = model
            for field in struct_def['fields']:
                field_name = field['name']
                field_descriptor = Field(**field, _model=model)
                fields.append(field_descriptor)
                attrs[field_name] = field_descriptor

            attrs['_Struct__fields'] = tuple(fields)
        # When the name of a field collides with a name
        # of a field from struct we store the value in
        # _Field__class_values and the field descriptor
        # will look it up when used on the class
        attrs['_Field__class_values'] = {}
        for field_name, value in struct_def.items():
            if field_name in root_ui_string:
                value = UiString(**value)

            if field_name in attrs:
                # The field descriptor know to check for this attribute
                # When being used on the class
                attrs['_Field__class_values'][field_name] = value
            else:
                attrs[field_name] = value

        return super().__new__(
            cls,
            name,
            final_bases,
            attrs,
        )

    def __repr__(cls):
        name = cls.name

        values = tuple(
            f'{name}={repr(getattr(cls, name, None))}'
            for name in struct_fields
        )
        values_str = ', '.join(values)

        return f'{name}({values_str})'


@public
def get_indiv_observable(indiv):
    return indiv._Struct__value_subject


@public
def indiv_fields(indiv):
    return indiv.__class__._Struct__fields


@public
def get_path(indiv):
    return indiv._Struct__path


@public
def get_model(indiv):
    return indiv._Struct__model


@public
def get_struct_name(indiv):
    return type(indiv).name


class Struct(
        metaclass=StructMeta,
        struct_def=struct_struct_def,
        is_base=True,
        model=None,
):
    def __init__(self, values=None, *, is_base=False, **kwargs):
        self.__path = DotPath()
        if values is None:
            values = {}

        values |= kwargs

        if not is_base:
            cls = self.__class__
            self._Field__field_info = {}

            self.__value_subjects = {}
            for field in cls.__fields:
                value_subject, = field.init_indiv(
                    self,
                    values.get(field.name, undefined),
                )
                self.__value_subjects[field.name] = value_subject

            self.__value_subject = combine_latest(
                *self.__value_subjects.values()
            ).pipe(
                map(lambda items: self)
            )

        super().__init__()

    def __repr__(self):
        cls = self.__class__
        name = cls.__name__

        values = tuple(
            f'{field.name}={repr(getattr(self, field.name, undefined))}'
            for field in cls.__fields
        )

        values_str = ', '.join(values)

        return f'{name}({values_str})'

    def __contains__(self, key):
        try:
            self[key]
        except IndexError:
            return False
        else:
            return True

    def __eq__(self, other):
        if not isinstance(other, Struct):
            return NotImplemented

        cls = self.__class__

        for field in cls.__fields:
            try:
                self_value = self[field.name]
            except IndexError:
                self_value = undefined

            try:
                other_value = other[field.name]
            except IndexError:
                other_value = undefined

            if self_value != other_value:
                return False
        else:
            return True

    def __getitem__(self, key):
        try:
            return getattr(self, key)
        except AttributeError as err:
            raise IndexError(*err.args) from None

    def __setitem__(self, key, value):
        try:
            return setattr(self, key, value)
        except AttributeError as err:
            raise IndexError(*err.args) from None

    def __delitem__(self, key):
        try:
            return delattr(self, key)
        except AttributeError as err:
            raise IndexError(*err.args) from None

    def __iter__(self):
        cls = self.__class__
        for field in cls.__fields:
            if field.name in self:
                yield field.name

    def __reversed__(self):
        cls = self.__class__
        for field in reversed(cls.__fields):
            if field.name in self:
                yield field.name

    def __copy__(self):
        cls = self.__class__
        values = {}
        for field in cls.__fields:
            try:
                values[field.name] = self[field.name]
            except IndexError:
                pass

        return cls(**values)

    def __set_path(self, path: DotPath):
        self.__path = path

    def __deepcopy__(self, memo):
        from copy import deepcopy
        cls = self.__class__
        values = {}
        for field in cls.__fields:
            try:
                values[field.name] = deepcopy(self[field.name], memo)
            except IndexError:
                pass

        return cls(**values)

    @classmethod
    async def load_file(cls, file: Path):
        return await run_sync(cls.load_file_sync, file)

    @classmethod
    def load_file_sync(cls, file: Path):
        model = cls.__model
        format = model.formats.by_suffix[file.suffix]
        with file.open() as file_obj:
            rec = format.load(file_obj)
            indiv = model.coerce_from(rec, format, cls.name)
            return indiv


@public
class StructRegistry(Registry):
    def __init__(self, model):
        super().__init__(model)

    def __call__(self, struct_def: Union[str, dict], *bases):
        if isinstance(struct_def, str):
            return self[struct_def]
        else:
            name = struct_def['name']
            return super().__call__(name,  StructMeta(
                name,
                chain((Struct, ), bases),
                {},
                struct_def=struct_def,
                model=self.__model,
            ))


class ChildField(Field, type='child'):
    def init_indiv(self, indiv, value=undefined):
        parent_path = get_path(indiv)
        path = parent_path | self.name
        struct_name = self.attrs['struct_name'].removeprefix('meta:')
        struct_cls = self._model.structs[struct_name]
        child_indiv = struct_cls(value)
        child_indiv._Struct__set_path(path)
        subject = get_indiv_observable(child_indiv)
        return super().init_indiv(indiv, child_indiv, _subject=subject)

    def __set__(self, parent_indiv, new_value):
        info = self.get_info(parent_indiv)
        indiv = info.current_value
        if new_value is not undefined:
            getter = (
                getitem
                if isinstance(new_value, Mapping)
                else getattr
            )

            for field in indiv_fields(indiv):
                try:
                    indiv[field.name] = getter(new_value, field.name)
                except (KeyError, AttributeError):
                    del indiv[field.name]
        else:
            for field in indiv_fields(indiv):
                del indiv[field.name]



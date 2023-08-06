from __future__ import annotations
from itertools import chain
from importlib import import_module
from pathlib import Path
from collections.abc import Mapping
from operator import getitem
from typing import TYPE_CHECKING

from ruamel.yaml import safe_load as load
from rx import combine_latest
from rx.operators import map

from .field import Field, UiString
from .undefined import undefined
from .dot_path import DotPath

if TYPE_CHECKING:
    from .model import Model

bases_path = DotPath(('implementation', 'python', 'bases'))
meta_model_path = Path(__file__).parent/'structs'
struct_def_path = meta_model_path/'struct.json'

# The struct def of struct
struct_struct_def = load(struct_def_path.open('r', encoding='utf8'))


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

        attrs['_Struct__model'] = model

        fields = []
        if not is_base:
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


def get_indiv_observable(indiv):
    return indiv._Struct__value_subject


def indiv_fields(indiv):
    return indiv.__class__._Struct__fields


def get_path(indiv):
    return indiv._Struct__path


def get_model(indiv):
    return indiv._Struct__model


def get_struct_name(indiv):
    return type(indiv).name


def create_struct(model):
    class Struct(
            metaclass=StructMeta,
            struct_def=struct_struct_def,
            model=model,
            is_base=True,
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

        def __eq__(self, other):
            if not isinstance(other, Struct):
                return NotImplemented

            cls = self.__class__

            for field in cls.__fields:
                self_value = self[field.name]
                other_value = other[field.name]
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
                yield field.name

        def __reversed__(self):
            cls = self.__class__
            for field in reversed(cls.__fields):
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

    return Struct


class StructRegistry(Mapping):
    def __init__(self, model):
        self.__model = model
        self.__struct = create_struct(self.__model)
        self.__structs = {}

    def __call__(self, struct_def, *bases):
        name = struct_def['name']
        self.__structs[name] = StructMeta(
            name,
            chain((self.__struct, ), bases),
            {},
            struct_def=struct_def,
            model=self.__model,
        )
        return self[name]

    def __getattr__(self, key):
        return self.__structs[key]

    def __getitem__(self, key):
        return self.__structs[key]

    def __iter__(self):
        return iter(self.__structs)

    def __len__(self):
        return len(self.__structs)

    def __contains__(self, struct_name):
        return struct_name in self.__structs

    def __repr__(self):
        cls = self.__class__
        name = cls.__name__
        values_str = ', '.join(self)

        return f'{name}({values_str})'


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



from collections.abc import Mapping, MutableMapping, MutableSequence, Callable
from typing import Any, Literal
from .field import Field
from .types import TypeExt, Adapter
from .dot_path import DotPath
from .validationResult import ValidationMessage, ValidationResult, ErrorTypes
from .undefined import undefined
from .localization import TXT
from dataclasses import asdict
from importlib import import_module


def create_adapter(direction: Literal['from_', 'to']):
    def adapt(self, format_name, value, type_name):
        adapters = self[type_name].adapters
        adapter = adapters[format_name]
        if adapter.native:
            return value

        if direction in adapter:
            converted_value = adapter[direction](value)
            return converted_value
        elif format_name != 'string':
            return adapt('string', value, type_name)


class TypeRegistry(Mapping, type):
    def __new__(cls, name, bases, attrs, model):
        attrs['_types'] = {}
        attrs['_model'] = model
        return super().__new__(cls, name, bases, attrs)

    def __repr__(cls):
        cls_name = cls.__class__.__name__
        types_repr = ', '.join(cls._types.keys())
        return f'{cls_name}({types_repr})'

    def __getitem__(cls, key):
        return cls._types[key]

    def __getattr__(cls, key):
        return cls[key]

    def __len__(cls):
        return len(cls.__dict__['_types'])

    def __iter__(cls):
        return iter(cls.__dict__['_types'])

    def __contains__(cls, item):
        return item in cls.__dict__['_types']

    def __reversed__(cls):
        return reversed(cls.__dict__['_types'])

    def __bool__(cls):
        return bool(cls.__dict__['_types'])

    def __call__(
        cls,
        name,
        implementation=None,
        adapters=None,
        validator=None,
        attributes=None,
        exts=None,
        *,
        standard=False,
    ):
        if name in cls and implementation is None:
            return cls[name]
        else:
            return super().__call__(
                name,
                implementation,
                adapters,
                validator,
                attributes,
                exts,
            )


def validate(*args, **kwargs):
    return True


def create_registry(model):
    class ModelType(metaclass=TypeRegistry, model=model):
        name: str
        impl: type
        adapters: MutableMapping[str, Adapter]
        validator: Callable[(Any, ), ValidationResult]
        attributes: MutableSequence[Field]
        exts: MutableSequence[TypeExt]

        def __new__(
            cls,
            name,
            implementation,
            validator,
            attributes,
            exts,
            standard=False,
        ):
            if name in cls._types:
                raise RuntimeError(
                    f'{name} has already been defined in type registry.'
                )
            else:
                instance = super().__new__(cls)
                cls._types[name] = instance
                return instance

        def __init__(
            self,
            name,
            implementation,
            adapters,
            validator,
            attributes,
            exts,
            standard=False,
        ):
            self.name = name
            self.impl = implementation
            self.adapters = adapters
            self.__validator = validator
            self.attributes = attributes
            self.exts = exts
            self.__standard = standard

        def __call__(self, *args, **kwargs):
            return self.impl(*args, **kwargs)

        def __repr__(self):
            impl = repr(self.impl)
            name = repr(self.name)
            return f'<RegisteredType name={name} implementation={impl}>'

        def __bool__(self):
            return True

        to_format = create_adapter('to')
        from_format = create_adapter('from_')

        def validate(
                self,
                value: Any,
                required: bool,
                path: DotPath,
                **attrs,
        ):
            if required and value is undefined:
                msg = ValidationMessage(
                    ErrorTypes.constraint_error,
                    f'"{path}" is required.',
                    path,
                )
                return ValidationResult(False, msg)
            elif not isinstance(value, self.impl):
                name = self.name
                txt = TXT(
                    '${value} is not valid for the type ${name}.',
                    locals(),
                )
                msg = ValidationMessage(ErrorTypes.invalid_value, txt, path)
                return ValidationResult(False, msg)

            else:
                return self.__validator(value, path, **attrs)

    def BuiltinModelType(type_name):
        module = import_module(f'.types.{type_name}', __package__)
        ModelType(standard=True, **asdict(module.type_def))

    BuiltinModelType('boolean')
    BuiltinModelType('binary')
    ModelType('estimate', float, validate, standard=True)
    BuiltinModelType('integer')
    BuiltinModelType('string')
    return ModelType

from abc import ABC, abstractmethod
from collections.abc import MutableMapping, Iterable, Mapping
from io import TextIOBase
from public import public


@public
class Localizable(ABC):
    @abstractmethod
    def localize(lang: str) -> str:
        pass


# Strings are considered localizeable so that double localization does not
# cause errors
Localizable.register(str)


format_preference = ('yaml', 'toml', 'json')


def pref_key(key):
    try:
        return format_preference.index(key)
    except IndexError:
        return len(format_preference)


@public
class Format(ABC):
    formats = {}
    formats_by_suffix = {}

    def __init_subclass__(cls, extension=None, mime_types=None, **kwargs):
        super().__init_subclass__(**kwargs)
        cls_name = cls.__name__
        name = cls_name.removesuffix('Format').lower()
        cls.name = name
        Format.formats[name] = cls
        Format.formats = {
            key: Format.formats[key]
            for key in sorted(Format.formats, key=pref_key)
        }

        if extension is None:
            cls.file_extension = name
        else:
            cls.file_extension = extension

        cls.file_suffix = f'.{cls.file_extension}'

        Format.formats_by_suffix[cls.file_suffix] = cls

        if mime_types is not None:
            mime_is_iter = (isinstance(mime_types, Iterable)
                            and not isinstance(mime_types, str))
            if mime_is_iter:
                mime_types = tuple(mime_types)
                cls.mime_types = frozenset(mime_types)
                cls.mime_type = mime_types[0]
            else:
                cls.mime_type = mime_types
                cls.mime_types = frozenset((mime_types, ))
        else:
            cls.mime_type = f'application/{name}'
            cls.mime_types = frozenset((cls.mime_type, ))

    @abstractmethod
    def load(self, file: TextIOBase) -> MutableMapping:
        pass

    @abstractmethod
    def loads(self, string: str) -> MutableMapping:
        pass

    @abstractmethod
    def dump(self, file: TextIOBase, data: dict) -> None:
        pass

    @abstractmethod
    def dumps(self, data: dict) -> str:
        pass

# loading these files will result in the classes being registered in Format
import omniblack.model.formats # noqa E402
import omniblack.model.extended_formats # noqa E402


@public
class FormatRegistry(Mapping):
    def __init__(self):
        super().__init__()
        self.__formats = {
            name: format()
            for name, format in Format.formats.items()
        }
        self.formats_by_suffix = {
            format.file_suffix: format
            for format in self.values()
        }

    def __repr__(self):
        cls_name = self.__class__.__name__
        formats_str = ', '.join(
            format
            for format in self.__formats
        )
        return f'{cls_name}({formats_str})'

    def __getattr__(self, key):
        try:
            return self.__formats[key]
        except IndexError as err:
            raise AttributeError(*err.args)

    def __iter__(self):
        return iter(self.__formats)

    def __len__(self):
        return len(self.__formats)

    def __contains__(self, key):
        return key in self.__formats



from .abc import Format
from io import TextIOBase, StringIO

try:
    import ruamel.yaml

except ImportError:
    pass
else:
    yaml_mime_types = (
        'text/vnd.yaml',
        'text/yaml',
        'text/x-yaml',
        'application/vnd.yaml',
        'application/yaml',
        'application/x-yaml',
    )

    class YamlFormat(Format, mime_types=yaml_mime_types):
        def __init__(self):
            self.loader = ruamel.yaml.YAML()

        def load(self, file: TextIOBase) -> dict:
            return self.loader.load(file)

        def loads(self, string: str) -> dict:
            stream = StringIO(string)
            return self.load(stream)

        def dump(self, file: TextIOBase, data: dict) -> None:
            self.loader.dump(data, file)

        def dumps(self, data: dict) -> str:
            stream = StringIO()
            self.loader.dump(data, stream)
            return stream.getvalue()

try:
    import toml
except ImportError:
    pass
else:
    class TomlFormat(Format):
        def load(self, file: TextIOBase) -> dict:
            return toml.load(file)

        def loads(self, string: str) -> dict:
            return toml.loads(string)

        def dump(self, file: TextIOBase, data: dict) -> None:
            toml.dump(data, file)

        def dumps(self, data: dict) -> str:
            return toml.dumps(data)

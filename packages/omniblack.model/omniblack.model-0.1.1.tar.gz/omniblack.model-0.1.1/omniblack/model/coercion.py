from .walker import visit_leaves, WalkerYield
from .mapper import map
from .struct import get_model
from .abc import Format
from typing import Union


def coerce_to(indiv, format: Union[str, Format]):
    if isinstance(format, Format):
        format_name = format.name
    else:
        format_name = format

    def to_map_cb(field: WalkerYield):
        type = field.field_def.type
        return model.types.to_format(format_name, field.value, type)
    model = get_model(indiv)

    return map(to_map_cb, indiv, visit_leaves)


def coerce_from(rec, format: Union[str, Format], struct_name, model):
    Struct = model.struct[struct_name]
    indiv = Struct(rec)

    if isinstance(format, Format):
        format_name = format.name
    else:
        format_name = format

    def from_map_cb(field: WalkerYield):
        type = field.field_def.type
        return model.types.from_format(format_name, field.value, type

    coerced_rec = map(from_map_cb, indiv, visit_leaves)

    return Struct(coerced_rec)

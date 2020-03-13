#coding=utf-8

from marshmallow import (
    Schema,
    fields,
    utils,
)

PRIMITIVE_TYPE_MAPPING = {
    fields.String: 'string',
    fields.UUID: 'string',
    fields.Integer: 'integer',
    fields.Boolean: 'bool',
    fields.Date: 'date-time',
    fields.DateTime: 'date-time',
    fields.Number: 'number',
    fields.Float: 'number',
}

OPTIONS_MAPPING = {
    'min': 'minimum',
    'max': 'maximum',
    'missing': 'default'
}


def parse_model(schema: Schema) -> dict:
    if isinstance(schema, fields.Field):
        return {
            'type': PRIMITIVE_TYPE_MAPPING.get(schema.__class__)
        }
    rv = dict()
    for field_name, field in schema._declared_fields.items():
        if isinstance(field, fields.Nested):
            nested_struct = parse_model(field.nested)
            if field.many:
                if isinstance(field.nested, fields.Field):
                    rv[field_name] = {
                        'type': 'array',
                        'items': {
                            'type': PRIMITIVE_TYPE_MAPPING.get(field.nested.__class__)
                        }
                    }
                else:
                    rv[field_name] = _process_array_field(nested_struct)
            else:
                rv[field_name] = _process_object_field(nested_struct)
        else:
            rv[field_name] = {
                'type': PRIMITIVE_TYPE_MAPPING.get(field.__class__)
            }
    return rv


def _process_object_field(data: dict) -> dict:
    return {
        'type': 'object',
        'properties': data
    }


def _process_array_field(data: dict) -> dict:
    return {
        'type': 'array',
        'items': {
            'type': 'object',
            'properties': data
        }
    }


def parse_parameter(name: str, schema: Schema) -> dict:
    rv = dict()
    for key, field in schema._declared_fields.items():
        if isinstance(field, fields.Nested):
            raise ValueError('Field in parameters must be primitive type')
        rv[key] = PRIMITIVE_TYPE_MAPPING.get(field.__class__)
    return rv

#coding=utf-8

from marshmallow import (
    Schema,
    fields,
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


class Parser:
    @classmethod
    def parse_field(cls, field: fields.Field) -> dict:
        if isinstance(field, fields.Nested):
            nested = cls.parse_schema(field.nested)
            if field.many:
                return {
                    'type': 'array',
                    'items': nested
                }
            return nested
        return {
            'type': PRIMITIVE_TYPE_MAPPING.get(field.__class__)
        }

    @classmethod
    def parse_schema(cls, schema: Schema) -> dict:
        rv = dict()
        for name, field in schema._declared_fields.items():
            rv[name] = cls.parse_field(field)

        return {
            'type': 'object',
            'properties': rv
        }

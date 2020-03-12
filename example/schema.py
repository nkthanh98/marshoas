# coding=utf-8

# @Author   : nkthanh
# @Email    : nguyenkhacthanh244@gmail.com
# @Created  : 12/03/2020
# @License  : MIT

"""
schema.py
"""


from marshmallow import (
    Schema,
    fields,
    utils,
)


class Name(Schema):
    first = fields.String(required=True)
    last = fields.String(required=True)
    mid = fields.String()


class Job(Schema):
    title = fields.String(required=True)
    description = fields.String()


class Person(Schema):
    name = fields.Nested(Name())
    jobs = fields.Nested(Job(), many=True)
    age = fields.Integer(missing=5)


class GenericProduct(Schema):
    class Brand(Schema):
        id = fields.Integer()
        name = fields.String()

    class AttributeSet(Schema):
        id = fields.Integer()
        name = fields.String()

    id = fields.Integer()
    spu = fields.String()
    name = fields.String(min_len=1, max_len=265, required=True)
    master_category_id = fields.Integer()
    attribute_set = fields.Nested(AttributeSet())
    brand = fields.Nested(Brand())
    model = fields.String(max_len=255)
    unit_id = fields.Integer(required=True)
    unit_po_id = fields.Integer()
    tax_in_code = fields.String(required=True)
    tax_out_code = fields.String(required=True)
    warranty_months = fields.Integer(min_val=0, required=True, strict=True)
    warranty_note = fields.String(max_len=255)
    detailed_description = fields.String()
    description = fields.String(max_len=500)
    type = fields.String()
    editing_status_code = fields.String()
    url_key = fields.String()
    updated_at = fields.DateTime()
    created_at = fields.DateTime()
    created_by = fields.String()
    updated_by = fields.String()


class ListPerson(Schema):
    people = fields.Nested(Person(), many=True)
    ns = fields.Nested(fields.Integer(), many=True)

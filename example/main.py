# coding=utf-8

# @Author   : nkthanh
# @Email    : nguyenkhacthanh244@gmail.com
# @Created  : 12/03/2020
# @License  : MIT

"""
main.py
"""

import json
import marshoas
import schema


data = marshoas.parser.parse_model(schema.Person())

spec = marshoas.OpenAPI()
ops = marshoas.Operation()
ops.add_response(data, status_code=400, schema_type="application/json")
spec.add_operation('/products', ops)
print(json.dumps(spec.to_json()))

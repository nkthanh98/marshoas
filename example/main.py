# coding=utf-8

# @Author   : nkthanh
# @Email    : nguyenkhacthanh244@gmail.com
# @Created  : 12/03/2020
# @License  : MIT

"""
main.py
"""

import json
from marshoas import parser
import schema


data = parser.parse_model(schema.Person())
print(json.dumps(data))

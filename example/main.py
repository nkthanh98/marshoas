# coding=utf-8

# @Author   : nkthanh
# @Email    : nguyenkhacthanh244@gmail.com
# @Created  : 12/03/2020
# @License  : MIT

"""
main.py
"""

import marshoas
import schema


app = marshoas.Application(
    __name__,
    url_doc='/docs',
    title='lmao',
    version='0.0.0'
)
ns = marshoas.Namespace('lmao', __name__)

@ns.resource('/lmao')
class Lmao(marshoas.Resource):
    @ns.response(schema.GenericProduct)
    def get(self):
        return 'DMM'

app.register_blueprint(ns, url_prefix='/dmm')

if __name__ == '__main__':
    app.run()

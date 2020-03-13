#coding=utf-8

import os
import typing as T
from werkzeug.routing import parse_rule
from flask import (
    Flask,
    Blueprint,
    jsonify,
    current_app,
    send_file
)
from flask.views import MethodView
from marshmallow import (
    Schema,
    fields,
)
from .oas import (
    OpenAPI,
    Operation
)
from ._globals import spec



def doc_render_fn():
    return send_file(os.path.join(
        os.path.dirname(__file__),
        'doc.html'
    ))


def openapi_fn():
    return jsonify(**spec.to_dict())


class Resource(MethodView):
    def dispatch_request(self, *args, **kwargs):
        # validate request

        resp = super().dispatch_request(*args, **kwargs)
        # marshall response
        return resp



class Namespace(Blueprint):
    app: Flask = None

    def resource(self, rule, **options) -> T.Callable:
        def decorator(res: Resource) -> T.Callable:
            endpoint = options.pop("endpoint", res.__name__)
            self.add_url_rule(rule, endpoint, view_func=res.as_view(endpoint), **options)
            return res
        return decorator

    def response(self, schema: Schema, many=False):
        def decorator(f: T.Callable) -> T.Callable:
            return f

        op = Operation()
        op.add_response(schema())
        spec.add_operation('/products', op)

        return decorator


class Application(Flask):
    def __init__(self, *args, **kwargs):
        url_doc = kwargs.pop('url_doc', False)
        spec.title = kwargs.pop('title', 'OpenAPIv3')
        spec.description = kwargs.pop('description', '')
        spec.version = kwargs.pop('version', '1.0.0')
        super().__init__(*args, **kwargs)
        if url_doc:
            self.add_url_rule(url_doc, doc_render_fn.__name__, doc_render_fn)
            self.add_url_rule(f'{url_doc}/openapi.json', openapi_fn.__name__, openapi_fn)

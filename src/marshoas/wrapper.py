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
from .oas import OpenAPI



def doc_render_fn():
    return send_file(os.path.join(
        os.path.dirname(__file__),
        'doc.html'
    ))


def openapi_fn():
    return jsonify(**current_app._spec.to_dict())


class Resource(MethodView):
    pass


class Namespace(Blueprint):
    def resource(self, rule, **options) -> T.Callable:
        def decorator(res: Resource) -> T.Callable:
            endpoint = options.pop("endpoint", res.__name__)
            self.add_url_rule(rule, endpoint, view_func=res.as_view(endpoint), **options)
            return res
        return decorator


class Application(Flask):
    def __init__(self, *args, **kwargs):
        url_doc = kwargs.pop('url_doc', False)
        super().__init__(*args, **kwargs)
        if url_doc:
            self.add_url_rule(url_doc, doc_render_fn.__name__, doc_render_fn)
            self.add_url_rule(f'{url_doc}/openapi.json', openapi_fn.__name__, openapi_fn)
        self._spec = OpenAPI()

#coding=utf-8

import typing as T
import json
from marshmallow import Schema
from marshoas import parser


class Operation:
    def __init__(
            self,
            method: str = 'get',
            summary: str = "",
            description: str = "",
            op_id: str = ""
    ):
        self.method: str = method
        self.summary: str = summary
        self.description: str = description
        self.op_id: str = op_id
        self.parameters: T.List[dict] = list()
        self.request_body: dict = dict()
        self.responses: T.Dict[int, dict] = dict()
        self.schema = None

    def add_response(
            self,
            schema_or_dict=None,
            status_code=200,
            schema_type="application/json",
            description="",
    ):
        if schema_or_dict:
            assert isinstance(schema_or_dict, (dict, Schema)), \
                'Schema of response must be instance of dict or marshmallow.Schema'
        if status_code in self.responses:
            raise ValueError('Can\'t add response because status code existed')

        self.responses[status_code] = {
            'description': description,
            'schema_type': schema_type,
            'schema': schema_or_dict
        }

    def to_json(self) -> dict:
        responses = dict()
        for code, resp in self.responses.items():
            responses[code] = {
                'description': resp['description'],
                'content': {
                    resp['schema_type']: {
                        'schema': resp['schema'] if isinstance(resp, dict) else parser.parse_model(resp['schema'])
                    }
                }
            }
        return {
            'summary': self.summary,
            'description': self.description,
            'responses': responses
        }


class OpenAPI:
    def __init__(
            self,
            title: str = "OpenAPIv3",
            description: str = "",
            version: str = "1.0.0"
    ):
        self.title: str = title
        self.description: str = description
        self.version: str = version
        self.servers: T.List[T.Dict[str, str]] = list()
        self.paths: T.Dict[str, T.List[Operation]] = dict()

    def add_server(
            self,
            url: str,
            description: str = ""
    ):
        self.servers.append({
            'url': url,
            'description': description
        })

    def add_operation(
            self,
            url: str,
            operation: Operation
    ):
        if url not in self.paths:
            self.paths[url] = list()
        self.paths[url].append(operation)

    def to_json(self, dump: bool = False):
        paths_json = dict()
        rv = {
            'openapi': "3.0.0",
            'info': {
                'title': self.title,
                'description': self.description,
                'version': self.version
            },
            'servers': self.servers,
            'paths': paths_json
        }
        for url, operations in self.paths.items():
            ops_json = dict()
            for op in operations:
                ops_json[op.method] = op.to_json()
            paths_json[url] = ops_json

        if dump:
            return json.dumps(rv)
        return rv

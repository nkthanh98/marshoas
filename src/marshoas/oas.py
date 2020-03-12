#coding=utf-8

import typing as T
import json


class Operation:
    def __init__(
            self,
            method: str = 'get',
            summary: str = None,
            description: str = None,
            op_id: str = None
    ):
        self.method: str = method
        self.summary: str = summary
        self.description: str = description
        self.op_id: str = op_id
        self.parameters: T.List[dict] = list()
        self.request_body: dict = dict()
        self.responses: T.Dict[int, dict] = dict()

    def add_parameter(
            self,
            parameter: dict
    ):
        self.parameters.append(parameter)

    def add_response(
            self,
            status_code,
            response
    ):
        if status_code in self.responses:
            raise ValueError('Can\'t add response because status code existed')
        self.responses[status_code] = response


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
            'openapi': self.version,
            'info': {
                'title': '3.0.0',
                'description': self.description,
                'version': self.version
            },
            'servers': self.servers,
            'paths': paths_json
        }
        for url, operations in self.paths.items():
            ops_json = dict()
            for op in operations:
                ops_json[op] = {
                    'summary': op.summary,
                    'description': op.description,
                    'responses': op.responses
                }
            paths_json[url] = ops_json

        if dump:
            return json.dumps(rv)
        return rv

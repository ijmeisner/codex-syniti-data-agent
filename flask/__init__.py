class Request:
    def __init__(self, json=None):
        self._json = json or {}

    def get_json(self, force=False):
        return self._json


class Response:
    def __init__(self, data, status_code=200):
        self.json = data
        self.status_code = status_code


def jsonify(data):
    return Response(data)


request = Request()


class Flask:
    def __init__(self, name):
        self.name = name
        self._routes = {}

    def route(self, path, methods=None):
        if methods is None:
            methods = ['GET']
        methods = tuple(m.upper() for m in methods)

        def decorator(func):
            self._routes[(path, methods)] = func
            return func

        return decorator

    def test_client(self):
        return TestClient(self)

    def run(self, host='127.0.0.1', port=5000):
        print(f"Running on {host}:{port} (stub)")


class TestClient:
    def __init__(self, app: Flask):
        self.app = app

    def post(self, path, json=None):
        for (p, methods), func in self.app._routes.items():
            if p == path and 'POST' in methods:
                request._json = json or {}
                result = func()
                if isinstance(result, tuple):
                    resp, status = result
                else:
                    resp, status = result, 200
                if not isinstance(resp, Response):
                    resp = Response(resp, status)
                resp.status_code = status
                return resp
        return Response(None, 404)


# Provide testing submodule with FlaskClient
import types

testing = types.SimpleNamespace(FlaskClient=TestClient)

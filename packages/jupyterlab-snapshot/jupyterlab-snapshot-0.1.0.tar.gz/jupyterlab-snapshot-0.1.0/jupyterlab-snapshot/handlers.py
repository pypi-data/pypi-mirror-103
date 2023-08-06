import json
import os

from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
import tornado

class ExampleHandler(APIHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def get(self):
        self.finish(json.dumps({
            "data": "This is /jupyterlab-snapshot/get_example endpoint!"
        }))


class SnapshotHandler(APIHandler):

    @property
    def snapshotmanager(self):
        return self.settings['snapshotmanager']


class SaveSnapshotHandler(SnapshotHandler):

    @tornado.web.authenticated
    async def post(self):
        json_body = self.get_json_body()
        path = json_body['path']

        nb_ext = os.path.splitext(path)[1]
        if nb_ext != '.ipynb':
            raise web.HTTPError(500, f'snapshot file[{path}] must be notebook')

        model = self.contents_manager.get(path)
        if model['type'] != 'notebook':
            raise web.HTTPError(500, f'snapshot file[{path}] must be notebook')

        nb = model['content']
        nb_name = os.path.splitext(model['name'])[0]
        self.snapshotmanager.put(path, nb)


class GetSnapshotsInfoHandler(IPythonHandler):

    @tornado.web.authenticated
    async def get(self):
        pass


class GetSnapshotDiffHandler(IPythonHandler):

    @tornado.web.authenticated
    async def get(self):
        pass



handlers = [
    (r'/snapshot/save', SaveSnapshotHandler),
    (r'/snapshot/list', GetSnapshotsInfoHandler),
    (r'/snapshot/diff', GetSnapshotDiffHandler),
    (r'/snapshot/example', ExampleHandler),
]


def setup_handlers(web_app):
    host_pattern = ".*$"

    base_url = web_app.settings["base_url"]
    route_pattern = url_path_join(base_url, "snapshot", "get_example")
    handlers = [(url_path_join(base_url, handler[0]), handler[1]) for handler in handlers]
    web_app.add_handlers(host_pattern, handlers)

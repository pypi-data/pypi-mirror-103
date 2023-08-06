from notebook.base.handlers import IPythonHandler
from tornado import web

import os


class SnapshotHandler(IPythonHandler):

    @property
    def snapshotmanager(self):
        return self.settings['snapshotmanager']


class SaveSnapshotHandler(SnapshotHandler):
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
    async def get(self):
        pass


class GetSnapshotDiffHandler(IPythonHandler):
    async def get(self):
        pass


handlers = [
    (r'/snapshot/save', SaveSnapshotHandler),
    (r'/snapshot/list', GetSnapshotsInfoHandler)
]

from traitlets import default, Type, Instance, Dict
from traitlets.config.configurable import LoggingConfigurable

from .filemanager import LocalFileManager, FileManager


class SnapshotManager(LoggingConfigurable):

    filemanager = Instance(klass=FileManager, config=True)

    @default('filemanager')
    def _default_filemanager(self):
        return LocalFileManager

    def save_snapshot(self, path, content):
        raise NotImplementedError

    def get_snapshot(self, path):
        raise NotImplementedError

    def delete_snapshot(self, path):
        raise NotImplementedError

    def duplicate_snapshot(self, src_path, dest_path):
        raise NotImplementedError

    def snapshots_diff(self):
        raise NotImplementedError



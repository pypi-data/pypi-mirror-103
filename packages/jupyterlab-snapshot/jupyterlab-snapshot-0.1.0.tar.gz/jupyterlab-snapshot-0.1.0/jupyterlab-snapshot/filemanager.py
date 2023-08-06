import json
import mimetypes
import os
import shutil
import sys
from datetime import datetime

import nbformat
from nbformat import validate as validate_nb, ValidationError
from notebook import _tz as tz
from notebook.utils import exists, to_os_path
from notebook.services.contents.fileio import FileManagerMixin
from send2trash import send2trash, TrashPermissionError
from tornado import web
from tornado.web import HTTPError
from traitlets import Bool, Unicode, default
from traitlets.config.configurable import LoggingConfigurable


class FileManager(LoggingConfigurable):

    def save(self, model, path=''):
        raise NotImplementedError

    def get(self, path, content=True, type=None, format=None):
        raise NotImplementedError

    def delete(self, path):
        raise NotImplementedError

    def exists(self, path):
        raise NotImplementedError

    def file_exists(self, path):
        raise NotImplementedError

    def dir_exists(self, path):
        raise NotImplementedError


class LocalFileManager(FileManager, FileManagerMixin):

    delete_to_trash = Bool(True, config=True,
                           help="""If True (default), deleting files will send them to the
                                   platform's trash/recycle bin, where they can be recovered. If False,
                                   deleting files really deletes them.""")

    root_dir = Unicode(config=True)

    @default('root_dir')
    def _default_root_dir(self):
        return os.getcwd()

    def validate_notebook_model(self, model):
        """Add failed-validation message to model"""
        try:
            validate_nb(model['content'])
        except ValidationError as e:
            model['message'] = u'Notebook validation failed: {}:\n{}'.format(
                e.message, json.dumps(e.instance, indent=1, default=lambda obj: '<UNKNOWN>'),
            )
        return model

    def save(self, model, path=''):
        """Save the file model and return the model with no content."""
        path = path.strip('/')

        if 'type' not in model:
            raise web.HTTPError(400, u'No file type provided')
        if 'content' not in model:
            raise web.HTTPError(400, u'No file content provided')

        os_path = self._get_os_path(path)
        self.log.debug("Saving %s", os_path)

        try:
            if model['type'] == 'notebook':
                nb = nbformat.from_dict(model['content'])
                self._save_notebook(os_path, nb)
            else:
                raise web.HTTPError(400, "Unhandled contents type: %s" % model['type'])
        except web.HTTPError:
            raise
        except Exception as e:
            self.log.error(u'Error while saving file: %s %s', path, e, exc_info=True)
            raise web.HTTPError(500, u'Unexpected error while saving file: %s %s' %
                                (path, e)) from e

        validation_message = None
        if model['type'] == 'notebook':
            self.validate_notebook_model(model)
            validation_message = model.get('message', None)

        model = self.get(path, content=False)
        if validation_message:
            model['message'] = validation_message

        return model

    def _base_model(self, path):
        """Build the common base of a contents model"""
        os_path = self._get_os_path(path)
        info = os.lstat(os_path)

        try:
            # size of file
            size = info.st_size
        except (ValueError, OSError):
            self.log.warning('Unable to get size.')
            size = None

        try:
            last_modified = tz.utcfromtimestamp(info.st_mtime)
        except (ValueError, OSError):
            # Files can rarely have an invalid timestamp
            # https://github.com/jupyter/notebook/issues/2539
            # https://github.com/jupyter/notebook/issues/2757
            # Use the Unix epoch as a fallback so we don't crash.
            self.log.warning('Invalid mtime %s for %s', info.st_mtime, os_path)
            last_modified = datetime(1970, 1, 1, 0, 0, tzinfo=tz.UTC)

        try:
            created = tz.utcfromtimestamp(info.st_ctime)
        except (ValueError, OSError):  # See above
            self.log.warning('Invalid ctime %s for %s', info.st_ctime, os_path)
            created = datetime(1970, 1, 1, 0, 0, tzinfo=tz.UTC)

        # Create the base model.
        model = {}
        model['name'] = path.rsplit('/', 1)[-1]
        model['path'] = path
        model['last_modified'] = last_modified
        model['created'] = created
        model['content'] = None
        model['format'] = None
        model['mimetype'] = None
        model['size'] = size

        try:
            model['writable'] = os.access(os_path, os.W_OK)
        except OSError:
            self.log.error("Failed to check write permissions on %s", os_path)
            model['writable'] = False
        return model

    def _file_model(self, path, content=True, format=None):
        """Build a model for a file

        if content is requested, include the file contents.

        format:
          If 'text', the contents will be decoded as UTF-8.
          If 'base64', the raw bytes contents will be encoded as base64.
          If not specified, try to decode as UTF-8, and fall back to base64
        """
        model = self._base_model(path)
        model['type'] = 'file'

        os_path = self._get_os_path(path)
        model['mimetype'] = mimetypes.guess_type(os_path)[0]

        if content:
            content, format = self._read_file(os_path, format)
            if model['mimetype'] is None:
                default_mime = {
                    'text': 'text/plain',
                    'base64': 'application/octet-stream'
                }[format]
                model['mimetype'] = default_mime

            model.update(
                content=content,
                format=format,
            )

        return model

    def _notebook_model(self, path, content=True):
        """Build a notebook model

        if content is requested, the notebook content will be populated
        as a JSON structure (not double-serialized)
        """
        model = self._base_model(path)
        model['type'] = 'notebook'
        os_path = self._get_os_path(path)

        if content:
            nb = self._read_notebook(os_path, as_version=4)
            self.mark_trusted_cells(nb, path)
            model['content'] = nb
            model['format'] = 'json'
            self.validate_notebook_model(model)
        return model

    def get(self, path, content=True, type=None, format=None):
        """ Takes a path for an entity and returns its model

        Parameters
        ----------
        path : str
            the API path that describes the relative path for the target
        content : bool
            Whether to include the contents in the reply
        type : str, optional
            The requested type - 'file', 'notebook', or 'directory'.
            Will raise HTTPError 400 if the content doesn't match.
        format : str, optional
            The requested format for file contents. 'text' or 'base64'.
            Ignored if this returns a notebook or directory model.

        Returns
        -------
        model : dict
            the contents model. If content=True, returns the contents
            of the file or directory as well.
        """
        path = path.strip('/')

        if not self.exists(path):
            raise web.HTTPError(404, u'No such file or directory: %s' % path)

        os_path = self._get_os_path(path)
        if os.path.isdir(os_path):
            raise web.HTTPError(400, u'%s is a directory, not a file' % path, reason='bad type')
        elif type == 'notebook' or (type is None and path.endswith('.ipynb')):
            model = self._notebook_model(path, content=content)
        else:
            if type == 'directory':
                raise web.HTTPError(400, u'%s is not a directory' % path, reason='bad type')
            model = self._file_model(path, content=content, format=format)
        return model

    def delete(self, path):
        """Delete file at path."""
        path = path.strip('/')
        os_path = self._get_os_path(path)
        rm = os.unlink
        if not os.path.exists(os_path):
            raise web.HTTPError(404, u'File or directory does not exist: %s' % os_path)

        def is_non_empty_dir(os_path):
            if os.path.isdir(os_path):
                if os.listdir(os_path):
                    return True
            return False

        if self.delete_to_trash:
            if sys.platform == 'win32' and is_non_empty_dir(os_path):
                # send2trash can really delete files on Windows, so disallow
                # deleting non-empty files. See Github issue 3631.
                raise web.HTTPError(400, u'Directory %s not empty' % os_path)
            try:
                self.log.debug("Sending %s to trash", os_path)
                send2trash(os_path)
                return
            except TrashPermissionError as e:
                self.log.warning("Skipping trash for %s, %s", os_path, e)

        if os.path.isdir(os_path):
            # Don't permanently delete non-empty directories.
            if is_non_empty_dir(os_path):
                raise web.HTTPError(400, u'Directory %s not empty' % os_path)
            self.log.debug("Removing directory %s", os_path)
            with self.perm_to_403():
                shutil.rmtree(os_path)
        else:
            self.log.debug("Unlinking file %s", os_path)
            with self.perm_to_403():
                rm(os_path)

    def file_exists(self, path):
        """Returns True if the file exists, else returns False.

        API-style wrapper for os.path.isfile

        Parameters
        ----------
        path : string
            The relative path to the file (with '/' as separator)

        Returns
        -------
        exists : bool
            Whether the file exists.
        """
        path = path.strip('/')
        os_path = self._get_os_path(path)
        return os.path.isfile(os_path)

    def dir_exists(self, path):
        """Does the API-style path refer to an extant directory?

        API-style wrapper for os.path.isdir

        Parameters
        ----------
        path : string
            The path to check. This is an API path (`/` separated,
            relative to root_dir).

        Returns
        -------
        exists : bool
            Whether the path is indeed a directory.
        """
        path = path.strip('/')
        os_path = self._get_os_path(path=path)
        return os.path.isdir(os_path)

    def exists(self, path):
        """Returns True if the path exists, else returns False.

        API-style wrapper for os.path.exists

        Parameters
        ----------
        path : string
            The API path to the file (with '/' as separator)

        Returns
        -------
        exists : bool
            Whether the target exists.
        """
        path = path.strip('/')
        os_path = self._get_os_path(path=path)
        return exists(os_path)

    def _get_os_path(self, path):
        """Given an API path, return its file system path.

        Parameters
        ----------
        path : string
            The relative API path to the named file.

        Returns
        -------
        path : string
            Native, absolute OS path to for a file.

        Raises
        ------
        404: if path is outside root
        """
        root = os.path.abspath(self.root_dir)
        os_path = to_os_path(path, root)
        if not (os.path.abspath(os_path) + os.path.sep).startswith(root):
            raise HTTPError(404, "%s is outside root contents directory" % path)
        return os_path


# class S3FileManager(FileManager):
#     def save(self, path, content):
#         pass
#
#     def get(self, path):
#         pass
#
#     def mv(self, from_path, to_path):
#         pass
#
#     def copy(self, src, dest):
#         pass
#
#     def delete_file(self, path):
#         pass
#
#     def delete_dir(self, path):
#         pass
#
#     def exists(self, path):
#         pass
#
#
# class OSS2FileManager(FileManager):
#     def save(self, path, content):
#         pass
#
#     def get(self, path):
#         pass
#
#     def mv(self, from_path, to_path):
#         pass
#
#     def copy(self, src, dest):
#         pass
#
#     def delete_file(self, path):
#         pass
#
#     def delete_dir(self, path):
#         pass
#
#     def exists(self, path):
#         pass

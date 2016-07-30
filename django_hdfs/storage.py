import os
import tempfile

from django.conf import settings
from django.core.files import File
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from hdfs import InsecureClient
from hdfs.util import HdfsError


@deconstructible
class HDFSStorage(Storage):
    """
    HDFS storage
    """

    def fix_slashes(self, path):
        sep = os.path.sep
        if path[0] != sep:
            path = sep + path
        if path[-1] != sep:
            path = path + sep
        return path

    def __init__(self, location=None, base_url=None):
        self.hdfs_hosts = settings.HDFS_STORAGE['hosts']
        self.hdfs_root = self.fix_slashes(settings.HDFS_STORAGE['root'])
        self.media_root = settings.MEDIA_ROOT
        self.media_url = self.fix_slashes(settings.MEDIA_URL)

        self.fetch_url = '%s/webhdfs/v1%s%%s?op=OPEN' % (self.hdfs_hosts.split(',')[0], self.hdfs_root)
        self.client = InsecureClient(self.hdfs_hosts)

    def _open(self, name, mode='rb'):
        local_path = os.path.join(settings.MEDIA_ROOT, name.replace('/', os.path.sep))
        if not os.path.exists(local_path):
            remote_path = self.path(name)
            local_dir = os.path.dirname(local_path)
            if not os.path.exists(local_dir):
                os.mkdir(local_dir)
            print self.client.download(remote_path, local_path=local_path, overwrite=True,
                                       temp_dir=tempfile.gettempdir())
        return File(open(local_path, mode))

    def _save(self, name, content):
        print "_save(%s, %s, %s)" % (self, name, content)
        local_path = content.name
        hdfs_path = self.path(name)  # os.path.basename(local_path))
        print hdfs_path, local_path
        self.client.write(hdfs_path, data=content, overwrite=True)
        return name

    def url(self, name):
        return self.fetch_url % name

    def delete(self, name):
        return self.client.delete(self.path(name))

    def listdir(self, path):
        file_list = []
        dir_list = []
        for name, status in self.client.list(self.path(path), status=True):
            if status['type'] == 'DIRECTORY':
                dir_list.append(name)
            elif status['type'] == 'FILE':
                file_list.append(name)
        return dir_list, file_list

    def size(self, name):
        return self.client.status(self.path(name))['length']

    def exists(self, name):
        try:
            return True if self.client.status(self.path(name)) else False
        except HdfsError:
            return False

    def path(self, name):
        return (self.hdfs_root + name).replace('\\', '/')

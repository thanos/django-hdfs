 from django.conf import settings
from django.core.files.storage import Storage
from django.utils.six.moves.urllib.parse import urljoin
from django.utils.deconstruct import deconstructible
from django.core.files import File

from hdfs import InsecureClient
from hdfs.util import HdfsError

import tempfile

@deconstructible
class HDFSStorage(Storage):
    """
    HDFS storage
    """
    file_class = ContentFile
    def __init__(self, location=None, base_url=None):
        if location is None:
            location = settings.MEDIA_ROOT
        self.base_location = location
        self.location = self.base_location
        if base_url is None:
            base_url = settings.MEDIA_URL
        elif not base_url.endswith('/'):
            base_url += '/'
        self.base_url = base_url
        self.client = InsecureClient(settings.HDFS_HOST)

    def _open(self, name, mode='rb'):
        local_path=os.path.join(settings.MEDIA_ROOT, name)
        print self.client.download(self.path(name), local_path=settings.MEDIA_ROOT, overwrite=True, temp_dir=tempfile.gettempdir())
        return File(open(local_path, mode))

    def _save(self, name, content):
        print "_save(%s, %s, %s)" % (self, name, content)
        local_path=content.name
        hdfs_path = self.path(name) #os.path.basename(local_path))
        print hdfs_path, local_path
        return self.client.upload(hdfs_path, local_path, overwrite=True)

    def url(self, name):
        if self.base_url is None:
            raise ValueError("This file is not accessible via a URL.")
        return urljoin(self.base_url, filepath_to_uri(name))    

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
        return self.location + name

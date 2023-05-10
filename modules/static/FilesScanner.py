import hashlib
import os
from os import walk

from constants.constants import SERVICE_URL


class FilesScanner:

    init_path = ''
    parent = None

    def __init__(self, init_path, parent):
        if init_path:
            self.init_path = init_path
        else:
            self.init_path = os.path.abspath(os.curdir)
        self.parent = parent

    def md5(self, fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def sha1(self, fname):
        hash_sha1 = hashlib.sha1()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha1.update(chunk)
        return hash_sha1.hexdigest()

    def sha256(self, fname):
        hash_sha256 = hashlib.sha256()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    def check_files(self):

        def print_warning(path, id):
            print('Файл: {}. Подробнее - {}/ioc/{}'.format(path, SERVICE_URL, id))

        # self.parent.base_paths.append({'id': 12, 'ioc': 'C:\\Education\\NIR\\IOC Collector\\reaction-module\\test.txt'})

        [os.path.join(dirpath,f) for (dirpath, dirnames, filenames) in walk(self.init_path) for f in filenames]
        for (dirpath, dirnames, filenames) in walk(self.init_path):
            for file in filenames:
                full_path = os.path.abspath(os.path.join(dirpath, file))

                for ioc in self.parent.base_paths:
                    if ioc['ioc'] == full_path:
                        print_warning(full_path, ioc['id'])
                        break

                for ioc in self.parent.base_filenames:
                    if ioc['ioc'] == file:
                        print_warning(full_path, ioc['id'])
                        break

                for ioc in self.parent.base_md5:
                    if ioc['ioc'] == self.md5(full_path):
                        print_warning(full_path, ioc['id'])
                        break

                for ioc in self.parent.base_sha1:
                    if ioc['ioc'] == self.sha1(full_path):
                        print_warning(full_path, ioc['id'])
                        break

                for ioc in self.parent.base_sha256:
                    if ioc['ioc'] == self.sha256(full_path):
                        print_warning(full_path, ioc['id'])
                        break

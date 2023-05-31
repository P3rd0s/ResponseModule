import os
from os import walk

from constants.constants import SERVICE_URL
from modules.helpers.HashChecker import HashChecker


class FilesScanner:

    init_path = ''
    parent = None

    def __init__(self, init_path, parent):
        if init_path:
            self.init_path = init_path
        else:
            self.init_path = os.path.abspath(os.curdir)
        self.parent = parent

    def check_files(self):

        def print_warning(path, id):
            print('Файл: {}. Подробнее - {}/ioc/{}'.format(path, SERVICE_URL, id))

        def print_hash_warning(path, id, hash_type):
            print('Создан файл, {}: {}. Подробнее - {}/ioc/{}'.format(hash_type, path, SERVICE_URL, id))

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
                    if ioc['ioc'] == HashChecker.md5(full_path):
                        print_hash_warning(full_path, ioc['id'], 'MD5')
                        break

                for ioc in self.parent.base_sha1:
                    if ioc['ioc'] == HashChecker.sha1(full_path):
                        print_hash_warning(full_path, ioc['id'], 'SHA1')
                        break

                for ioc in self.parent.base_sha256:
                    if ioc['ioc'] == HashChecker.sha256(full_path):
                        print_hash_warning(full_path, ioc['id'], 'SHA256')
                        break

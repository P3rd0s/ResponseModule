import os
import re
import etw

from constants.constants import SERVICE_URL, FILE_PROVIDER, FILE_GUID
from modules.helpers.HashChecker import HashChecker


def print_warning(path, id):
    print('Создан файл: {}. Подробнее - {}/ioc/{}'.format(path, SERVICE_URL, id))


def print_hash_warning(path, id, hash_type):
    print('Создан файл, {}: {}. Подробнее - {}/ioc/{}'.format(hash_type, path, SERVICE_URL, id))


class FileCreationMonitor(etw.ETW):

    parent = None

    def __init__(self, parent):
        self.parent = parent
        # self.parent.base_filenames.append({'id': 12, 'ioc': 'New Text Document.txt'})
        providers = [etw.ProviderInfo(FILE_PROVIDER, etw.GUID(FILE_GUID))]
        super().__init__(providers=providers, event_callback=self.on_event, event_id_filters=[30])

    def on_event(self, x):
        data = x[1]
        pid = int(data['EventHeader']['ProcessId'])

        if pid != os.getpid():
            file_path = re.sub('^.*harddiskvolume.*?\\\\', '', data["FileName"], 0, re.IGNORECASE)

            for ioc in self.parent.base_paths:
                if file_path in ioc['ioc']:
                    print_warning(file_path, ioc['id'])
                    break

            for ioc in self.parent.base_filenames:
                if ioc['ioc'] in file_path:
                    print_warning(file_path, ioc['id'])
                    break

            try:
                for ioc in self.parent.base_md5:
                    if ioc['ioc'] == HashChecker.md5(file_path):
                        print_hash_warning(file_path, ioc['id'], 'MD5')
                        break

                for ioc in self.parent.base_sha1:
                    if ioc['ioc'] == HashChecker.sha1(file_path):
                        print_hash_warning(file_path, ioc['id'], 'SHA1')
                        break

                for ioc in self.parent.base_sha256:
                    if ioc['ioc'] == HashChecker.sha256(file_path):
                        print_hash_warning(file_path, ioc['id'], 'SHA256')
                        break
            except:
                pass

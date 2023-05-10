import os
import re
import etw

from constants.constants import SERVICE_URL, FILE_PROVIDER, FILE_GUID


def print_warning(path, id):
    print('Создан файл: {}. Подробнее - {}/ioc/{}'.format(path, SERVICE_URL, id))


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


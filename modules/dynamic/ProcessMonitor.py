import etw
import psutil

from constants.constants import PROCESS_PROVIDER, PROCESS_GUID, SERVICE_URL


def get_process(pid):
    process_name = ""
    process_name_cmdline = ""
    for proc in psutil.process_iter():
        if proc.pid == pid:
            process_name = proc.name()
            process_name_cmdline = " ".join(proc.cmdline())
    return process_name, process_name_cmdline


def print_warning(path, id):
    print('Процесс: {}. Подробнее - {}/ioc/{}'.format(path, SERVICE_URL, id))


class ProcessMonitor(etw.ETW):

    parent = None

    def __init__(self, parent):
        self.parent = parent
        # self.parent.base_filenames.append({'id': 12, 'ioc': 'idea64.exe'})
        # self.parent.base_filenames.append({'id': 13, 'ioc': 'com.docker.backend.exe'})
        # self.parent.base_filenames.append({'id': 14, 'ioc': 'cmd.exe'})
        providers = [etw.ProviderInfo(PROCESS_PROVIDER, etw.GUID(PROCESS_GUID))]
        super().__init__(providers=providers, event_callback=self.on_event, event_id_filters=[1])

    def on_event(self, x):
        data = x[1]
        pid = int(data['EventHeader']['ProcessId'])
        org_process_name, org_process_name_cmdline = get_process(pid)

        for ioc in self.parent.base_paths:
            if ioc['ioc'] in org_process_name_cmdline:
                print_warning(org_process_name_cmdline, ioc['id'])
                break

        for ioc in self.parent.base_filenames:
            if ioc['ioc'] == org_process_name:
                print_warning(org_process_name, ioc['id'])
                break


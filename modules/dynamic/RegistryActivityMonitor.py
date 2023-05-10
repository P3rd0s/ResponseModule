import etw

from constants.constants import SERVICE_URL, REGISTRY_PROVIDER, REGISTRY_GUID


def print_warning(path, id):
    print('Изменение реестра: {}. Подробнее - {}/ioc/{}'.format(path, SERVICE_URL, id))


class RegistryActivityMonitor(etw.ETW):
    parent = None

    def __init__(self, parent):
        self.parent = parent
        # self.parent.base_filenames.append({'id': 12, 'ioc': 'idea64.exe'})
        providers = [etw.ProviderInfo(REGISTRY_PROVIDER, etw.GUID(REGISTRY_GUID))]
        super().__init__(providers=providers, event_callback=self.on_event, event_id_filters=[1, 2, 3, 5])

    def on_event(self, x):
        data = x[1]
        path = None

        try:
            path = data['RelativeName'].lower()
        except KeyError:
            pass

        if not path:
            return

        for ioc in self.parent.base_registries:
            if ioc['ioc'][5:] == path:
                print_warning(path, ioc['id'])
                break

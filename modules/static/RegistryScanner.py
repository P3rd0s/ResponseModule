from winreg import ConnectRegistry, HKEY_LOCAL_MACHINE, OpenKey, HKEY_CURRENT_USER
from constants.constants import SERVICE_URL


class RegistryScanner:
    parent = None

    def __init__(self, parent):
        self.parent = parent

    def check_registry(self):
        for ioc in self.parent.base_registries:
            key = ioc['ioc']
            try:
                hkey = key[0:4]
                key_body = key[5:]

                if hkey == 'HKLM':
                    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
                    k = OpenKey(reg, key_body)
                    k.Close()
                elif hkey == 'HKCU':
                    reg = ConnectRegistry(None, HKEY_CURRENT_USER)
                    k = OpenKey(reg, key_body)
                    k.Close()

                print('Ключ реестра: {}. Подробнее - {}/ioc/{}'.format(key, SERVICE_URL, ioc['id']))

            except:
                pass

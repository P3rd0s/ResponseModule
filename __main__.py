import argparse
import re
import time

import requests

from multiprocessing import Process
from constants.constants import SERVICE_URL
from modules.dynamic.FileCreationMonitor import FileCreationMonitor
from modules.dynamic.ProcessMonitor import ProcessMonitor
from modules.dynamic.RegistryActivityMonitor import RegistryActivityMonitor
from modules.static.FilesScanner import FilesScanner
from modules.dynamic.NetworkMonitor import NetworkMonitor
from modules.static.RegistryScanner import RegistryScanner


def convert_ioc(ioc, with_paths = False):
    if with_paths:
        return {'id': ioc['id'], 'ioc': re.sub('(\\\\+)', '\\\\', ioc['ioc'].lower())}
    else:
        return {'id': ioc['id'], 'ioc': ioc['ioc'].lower()}


def convert_url(ioc):
    return {'id': ioc['id'], 'ioc': re.sub('\\[(.)\\]| ', '.', ioc['ioc'])}


class MonitorModule:
    base_md5 = []
    base_sha1 = []
    base_sha256 = []
    base_filenames = []
    base_paths = []
    base_registries = []
    base_URLs = []
    base_IPs = []
    base_Hosts = []

    def __init__(self):
        get_by_type_api = SERVICE_URL + '/api/iocs/getByType?type='

        self.base_md5 = list(map(lambda ioc: convert_ioc(ioc), requests.get(get_by_type_api + 'MD5').json()))
        self.base_sha1 = list(map(lambda ioc: convert_ioc(ioc), requests.get(get_by_type_api + 'SHA1').json()))
        self.base_sha256 = list(map(lambda ioc: convert_ioc(ioc), requests.get(get_by_type_api + 'SHA256').json()))
        self.base_filenames = list(map(lambda ioc: convert_ioc(ioc), requests.get(get_by_type_api + 'Filename').json()))
        self.base_paths = list(map(lambda ioc: convert_ioc(ioc, True), requests.get(get_by_type_api + 'Filepath').json()))
        self.base_registries = list(map(lambda ioc: convert_ioc(ioc, True), requests.get(get_by_type_api + 'Registry').json()))
        self.base_URLs = list(map(lambda ioc: convert_url(ioc), requests.get(get_by_type_api + 'URL').json()))
        self.base_IPs = list(map(lambda ioc: convert_url(ioc), requests.get(get_by_type_api + 'IP').json()))
        self.base_Hosts = list(map(lambda ioc: convert_url(ioc), requests.get(get_by_type_api + 'Host').json()))

    def scan_files(self):
        print('Сканирование файловой системы...\n')
        files_scanner = FilesScanner('', self)

        try:
            files_scanner.check_files()
            print('Сканирование файловой системы завершено\n')
        except KeyboardInterrupt:
            print('Сканирование файловой системы прервано\n')
        except Exception:
            print('[Ошибка] Сканирование файловой системы прервано\n')

    def monitor_network(self):
        print('Мониторинг сетевой активности...\n')
        network_monitor = NetworkMonitor(self)
        network_monitor.scan_network()

    def scan_registry(self):
        print('Сканирование реестра...\n')
        registry_scanner = RegistryScanner(self)

        try:
            registry_scanner.check_registry()
            print('Сканирование реестра завершено\n')
        except KeyboardInterrupt:
            print('Сканирование реестра прервано\n')
        except Exception:
            print('[Ошибка] Сканирование реестра прервано\n')

    def monitor_processes(self):
        print('Мониторинг процессов...\n')
        processes_monitor = ProcessMonitor(self)
        processes_monitor.start()

        try:
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            processes_monitor.stop()
            print('Мониторинг процессов окончен\n')
        except Exception:
            processes_monitor.stop()
            print('[Ошибка] Мониторинг процессов прерван\n')

    def monitor_files(self):
        print('Мониторинг файловой системы...\n')
        files_monitor = FileCreationMonitor(self)
        files_monitor.start()

        try:
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            files_monitor.stop()
            print('Мониторинг файловой системы окончен\n')
        except Exception:
            files_monitor.stop()
            print('[Ошибка] Мониторинг файловой системы прерван\n')

    def monitor_registry(self):
        print('Мониторинг реестра...\n')
        registry_monitor = RegistryActivityMonitor(self)
        registry_monitor.start()

        try:
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            registry_monitor.stop()
            print('Мониторинг реестра окончен\n')
        except Exception:
            registry_monitor.stop()
            print('[Ошибка] Мониторинг реестра прерван\n')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Модуль мониторинга и реанирования на индикаторы компрометации')
    parser.add_argument('--no-static', action='store_true', help='Полное сканирование системы')
    args = parser.parse_args()
    print(args.no_static)

    monitor = MonitorModule()

    dynamic_files = Process(target=monitor.monitor_files)
    dynamic_processes = Process(target=monitor.monitor_processes)
    dynamic_network = Process(target=monitor.monitor_network)
    dynamic_registry = Process(target=monitor.monitor_registry)
    static_files = None
    static_registry = None

    if not args.no_static:
        static_files = Process(target=monitor.scan_files)
        static_registry = Process(target=monitor.scan_registry)
        static_registry.start()
        static_files.start()

    dynamic_network.start()
    dynamic_files.start()
    dynamic_processes.start()
    dynamic_registry.start()

    try:
        dynamic_files.join()
        dynamic_processes.join()
        dynamic_network.join()
        dynamic_registry.join()

        if not args.no_static:
            static_files.join()
            static_registry.join()

    except KeyboardInterrupt:
        pass

import pyshark

from constants.constants import SERVICE_URL


class NetworkMonitor:

    parent = None

    def __init__(self, parent):
        self.parent = parent

    def scan_network(self):

        def print_warning(val, id):
            print('Сетевая активность: {}. Подробнее - {}/ioc/{}'.format(val, SERVICE_URL, id))

        network_interface = 'Беспроводная сеть'
        capture = pyshark.LiveCapture(network_interface)

        # print(psutil.net_if_addrs().keys())
        # self.parent.base_IPs.append({ 'ioc': '192.168.3.3', 'id': 222 })

        for packet in capture.sniff_continuously():
            try:
                protocol = packet.transport_layer
                dst_addr = packet.ip.dst
                url = packet[packet.highest_layer].qry_name

                for ioc in self.parent.base_IPs:
                    if ioc['ioc'] == dst_addr:
                        print_warning(dst_addr, ioc['id'])
                        break

                for ioc in self.parent.base_URLs:
                    if url in ioc['ioc']:
                        print_warning(url, ioc['id'])
                        break

                for ioc in self.parent.base_Hosts:
                    if ioc['ioc'] == url:
                        print_warning(url + ' Порт: ' + packet[protocol].srcport, ioc['id'])
                        break

            except AttributeError as e:
                pass

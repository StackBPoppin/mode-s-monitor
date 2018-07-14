from utils import bin2int, bin2hex
from abc import ABC, abstractmethod


class Router(ABC):
    """
    This class is responsible for taking a list of binary packets and passing them to the correct Downlink Format
    handler.
    When using this class, the routing_table must be populated, mapping Downlink Format numbers to the correct handlers
    """
    routing_table = {}

    @staticmethod
    def extract_data(packets):
        """
        Extract properties such as altitude, heading, airspeed etc. from a list of binary packets
        :param packets: A list of binary packets: eg. [[0, 1, 1, 0], [0, 0, 0, 1], [..]]
        :return: A dictionary mapping aircraft ICAO codes to properties: eg. {'AACCFF': {'altitude': 32000, ..}, ..}
        """
        data_extracted = {}

        for packet in packets:
            downlink_format = Router.__get_downlink_format(packet)

            if downlink_format in Router.routing_table:
                packet_decoded = Router.__decode_packet(Router.routing_table[downlink_format])

                if packet_decoded:
                    icao = Router.__get_icao(packet)

                    if icao in data_extracted:
                        data_extracted[icao].update(packet_decoded)
                    else:
                        data_extracted[icao] = packet_decoded

        return data_extracted

    @classmethod
    @abstractmethod
    def __decode_packet(cls, packet):
        pass

    @staticmethod
    def __get_downlink_format(packet):
        return bin2int(packet[0:5])

    @staticmethod
    def __get_icao(packet):
        return bin2hex(packet[8:32])

from router import Router
from utils import bin2int, crc


class DownlinkFormat17(Router):
    """
    This class handles Downlink Format 17 and 18
    """
    @classmethod
    def __decode_packet(cls, packet):
        """
        Runs a CRC check to ensure packet integrity, detects Type Code and decodes corresponding property
        :return: A dictionary containing property (Altitude, Airspeed etc.) and its value. eg: {'altitude': 32000}
        """
        if crc(packet) != 0:
            return None

        type_code = bin2int(packet[32:37])

        if 1 <= type_code <= 4:
            # Aircraft Callsign
            pass

        if 9 <= type_code <= 18:
            # Airborne Position
            pass

        if type_code == 19:
            # Aircraft Velocity
            pass

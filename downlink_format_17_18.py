from datetime import datetime
from math import sqrt, atan2, pi
from utils import bin2int, crc


class DownlinkFormat17:
    """
    This class handles Downlink Format 17 and 18
    """
    @classmethod
    def decode_packet(cls, packet):
        """
        Runs a CRC check to ensure packet integrity, detects Type Code and decodes corresponding property
        :return: A dictionary containing property (Altitude, Airspeed etc.) and its value. eg: {'altitude': 32000}
        """
        if crc(packet) != 0:
            return None

        type_code = bin2int(packet[32:37])

        if 1 <= type_code <= 4:
            return cls.__extract_call_sign(packet)

        if 9 <= type_code <= 18:
            position_dict = cls.__extract_position(packet)
            position_dict.update(cls.__extract_altitude(packet))
            return position_dict

        if type_code == 19:
            return cls.__extract_velocity(packet)

    @staticmethod
    def __extract_call_sign(packet):
        data_slice = packet[40:88]

        call_sign = ''
        for i in range(0, len(data_slice) - 5, 6):
            char_slice = data_slice[i:i + 6]
            char_code = bin2int(char_slice)

            if 1 <= char_code <= 26:
                call_sign += chr(char_code + 64)
            elif 48 <= char_code <= 57:
                call_sign += chr(char_code)

        return {'call_sign': call_sign}

    @staticmethod
    def __extract_position(packet):
        odd_bit = packet[53]
        latitude = bin2int(packet[54:71])
        longitude = bin2int(packet[71:88])
        latitude /= 131072.0
        longitude /= 131072.0

        if odd_bit:
            return {'lat_odd': latitude, 'lon_odd': longitude, 'odd_timestamp': datetime.now()}
        else:
            return {'lat_even': latitude, 'lon_even': longitude, 'even_timestamp': datetime.now()}

    @staticmethod
    def __extract_altitude(packet):
        altitude_slice = packet[40:52]
        altitude = bin2int(altitude_slice)

        q_bit = altitude_slice.pop(7)  # 1 = multiples of 25ft, 0 = multiples of 100ft

        if q_bit:
            altitude *= 25
        else:
            altitude *= 100

        altitude -= 1000

        return {'altitude': altitude}

    @staticmethod
    def __extract_velocity(packet):
        east_west_velocity_sign = packet[45]
        north_south_velocity_sign = packet[56]

        east_west_velocity = bin2int(packet[46:56])
        north_south_velocity = bin2int(packet[57:67])

        vertical_rate_sign = packet[68]
        vertical_rate = bin2int(packet[69:78])

        v_we = (east_west_velocity - 1)
        v_sn = (north_south_velocity - 1)

        if east_west_velocity_sign:
            v_we *= -1

        if north_south_velocity_sign:
            v_sn *= -1

        velocity_kts = sqrt((v_we ** 2) + (v_sn ** 2))
        heading = atan2(v_we, v_sn) * (360.0 / (2 * pi))

        if heading < 0:
            heading += 360

        vertical_rate = (vertical_rate - 1) * 64

        if vertical_rate_sign:
            vertical_rate *= -1

        return {'heading': heading, 'velocity': velocity_kts, 'vs': vertical_rate}

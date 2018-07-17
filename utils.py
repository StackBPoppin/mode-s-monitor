from math import floor, cos, acos, pi


def bin2int(binary_arr):
    binary_string = ''.join(str(x) for x in binary_arr)
    return int(binary_string, 2)


def bin2hex(binary_arr):
    return hex(bin2int(binary_arr))[2:]

"""
The implementation of nl, mod, crc and calc_lat_lon follows the steps found here:
http://mode-s.org/decode/adsb/compact-position-report.html
http://mode-s.org/decode/adsb/airborne-position.html
http://mode-s.org/decode/adsb/introduction.html#ads-b-checksum
"""


def crc(binary_packet, encode=False):
    # Work on a copy of the binary packet to not alter the original
    result_arr = binary_packet.copy()
    generator = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1]

    for i in range(0, len(result_arr) - 24):
        if not result_arr[i]:
            continue

        for x in range(0, len(generator)):
            result_arr[i+x] ^= generator[x]

    return bin2int(result_arr[-24:])


def nl(lat):
    if abs(lat) == 87:
        return 2

    if abs(lat) > 87:
        return 1

    num_zones = 15
    cos_nz = cos(pi / (2.0 * num_zones))
    cos_lat = cos((pi/180.0) * lat)
    bottom = acos(1 - ((1 - cos_nz) / (cos_lat ** 2)))

    return floor((2 * pi) / bottom)


def mod(x, y):
    return x - y * floor(x / y)


def calc_lat_lon(aircraft):
    j = floor(59 * aircraft['lat_even'] - 60 * aircraft['lat_odd'] + 0.5)

    d_lat_even = 360.0 / 60.0
    d_lat_odd = 360.0 / 59.0

    lat_even = d_lat_even * (mod(j, 60) + aircraft['lat_even'])
    lat_odd = d_lat_odd * (mod(j, 59) + aircraft['lat_odd'])

    if lat_even >= 270:
        lat_even -= 360

    if lat_odd >= 270:
        lat_odd -= 360

    if aircraft['even_timestamp'] >= aircraft['odd_timestamp']:
        latitude = lat_even
    else:
        latitude = lat_odd

    if nl(lat_even) != nl(lat_odd):
        return None

    if aircraft['even_timestamp'] > aircraft['odd_timestamp']:
        ni = max(nl(lat_even), 1)
        d_lon = 360.0 / ni
        m = floor(aircraft['lon_even'] * (nl(lat_even) - 1) - aircraft['lon_odd'] * nl(lat_even) + 0.5)
        lon = d_lon * (mod(m, ni) + aircraft['lon_even'])
    else:
        ni = max(nl(lat_odd) - 1, 1)
        d_lon = 360.0 / ni
        m = floor(aircraft['lon_even'] * (nl(lat_odd) - 1) - aircraft['lon_odd'] * nl(lat_odd) + 0.5)
        lon = d_lon * (mod(m, ni) + aircraft['lon_odd'])

    if lon >= 180:
        lon -= 360

    return {'latitude': latitude, 'longitude': lon}

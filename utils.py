def bin2int(binary_arr):
    binary_string = ''.join(str(x) for x in binary_arr)
    return int(binary_string, 2)


def bin2hex(binary_arr):
    return hex(bin2int(binary_arr))[2:]


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

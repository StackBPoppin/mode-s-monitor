def bin2int(binary_arr):
    binary_string = ''.join(str(x) for x in binary_arr)
    return int(binary_string, 2)


def bin2hex(binary_arr):
    return hex(bin2int(binary_arr))[2:]

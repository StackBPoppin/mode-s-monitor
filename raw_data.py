from numpy import abs as np_abs, median as np_median


class RawData:
    def __init__(self):
        """
        iq_data simply contains all raw samples from the SDR
        """
        self.iq_data = []

    def add_sample(self, iq_arr):
        """
        Add the iq samples to this instance's iq_data list
        :param iq_arr: A list containing raw iq data
        """
        self.iq_data.extend(iq_arr)

    def get_binary_packets(self):
        """
        Convert iq data to absolute values, detect noise threshold, detect mode-s preambles, convert to binary
        :return: A list containing binary packets, eg: [[0, 1, 1, 0], [1, 1, 1, 0], [..]]
        """
        abs_data = np_abs(self.iq_data)
        median = np_median(abs_data)
        noise_threshold = median + (median * 1.4826 * 4)
        preamble_indices = RawData.__detect_preambles(abs_data, noise_threshold)

        packets = []
        for index in preamble_indices:
            packet = []
            for i in range(index + 16, index + 240, 2):
                if abs_data[i] > abs_data[i + 1]:
                    packet.append(1)
                else:
                    packet.append(0)
            packets.append(packet)

        return packets

    @staticmethod
    def __detect_preambles(abs_data, noise_threshold):
        preamble_indices = []

        # Packet is 112 bits = 224 samples, + 16 preamble samples = 240 total size
        # Subtracting 239 because second parameter in range() is exclusive
        for offset in range(0, len(abs_data) - 239):
            if RawData.__is_preamble(abs_data[offset:offset + 16], noise_threshold):
                preamble_indices.append(offset)

        return preamble_indices

    @staticmethod
    def __is_preamble(potential_preamble, noise_threshold):
        high_bits = (0, 2, 7, 9,)

        for i in range(0, 16):
            if i in high_bits:
                if potential_preamble[i] < noise_threshold:
                    return False
            else:
                if potential_preamble[i] > noise_threshold:
                    return False

        return True

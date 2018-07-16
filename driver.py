from rtlsdr import RtlSdr
from raw_data import RawData
from router import Router
from downlink_format_17_18 import DownlinkFormat17
from utils import calc_lat_lon


class Driver:
    """
    global_aircraft_data is a dictionary where the key is an aircraft ICAO code
    and the value is a dictionary containing aircraft attributes (altitude, heading, etc.) mapped to values

    For example:
    global_aircraft_data = {'84AB6F': {'altitude': 36000, 'heading': 120, 'callsign': 'EZY1825'}, '66BBFF': {..}}
    """
    global_aircraft_data = {}

    @staticmethod
    def run():
        """
        This is the main routine:
        1) Capture data from SDR and add to a RawData object
        2) When enough samples are collected, extract binary packets
        3) Pass binary packets to Router, store results in global_aircraft_data
        4) Scan the global_aircraft_data dictionary for an aircraft containing both even and odd packets, calculate
        latitude and longitude
        5) Send global_aircraft_data to output handler
        """
        RAW_SAMPLES = 512000
        SAMPLES_PER_EXTRACTION = 4
        FREQUENCY = 1090000000
        GAIN = 297
        SAMPLE_RATE = 2000000

        sdr = RtlSdr()
        sdr.sample_rate = SAMPLE_RATE
        sdr.center_freq = FREQUENCY
        sdr.gain = GAIN

        Router.routing_table[17] = DownlinkFormat17.decode_packet
        Router.routing_table[18] = DownlinkFormat17.decode_packet

        while True:
            raw_data = RawData()

            for i in range(0, SAMPLES_PER_EXTRACTION):
                raw_data.add_sample(sdr.read_samples(RAW_SAMPLES))

            binary_packets = raw_data.get_binary_packets()
            extracted_properties = Router.extract_data(binary_packets)

            for icao in extracted_properties:
                if icao in Driver.global_aircraft_data:
                    Driver.global_aircraft_data[icao].update(extracted_properties[icao])
                else:
                    Driver.global_aircraft_data[icao] = extracted_properties[icao]

            for icao in Driver.global_aircraft_data:
                if all(key in Driver.global_aircraft_data[icao] for key in ['lat_even', 'lon_even', 'lat_odd', 'lon_odd']):
                    position = calc_lat_lon(Driver.global_aircraft_data[icao])

                    if position:
                        Driver.global_aircraft_data[icao].update(position)

            print(Driver.global_aircraft_data)

if __name__ == '__main__':
    Driver.run()

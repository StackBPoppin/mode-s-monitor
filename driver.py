class Driver:
    def __init__(self):
        """
        global_aircraft_data is a dictionary where the key is an aircraft ICAO code
        and the value is a dictionary containing aircraft attributes (altitude, heading, etc.) mapped to values

        For example:
        global_aircraft_data = {'84AB6F': {'altitude': 36000, 'heading': 120, 'callsign': 'EZY1825'}, '66BBFF': {..}}
        """
        self.global_aircraft_data = {}

    def run(self):
        """
        This is the main routine:
        1) Capture data from SDR and add to a RawData object
        2) When enough samples are collected, extract binary packets
        3) Pass binary packets to Router, store results in global_aircraft_data
        4) Scan the global_aircraft_data dictionary for an aircraft containing both even and odd packets, calculate
        latitude and longitude
        5) Send global_aircraft_data to output handler
        """



import curses
from collections import OrderedDict


class Output:
    __header_dict = OrderedDict({
        'ICAO': 0,
        'Call Sign': 8,
        'Alt ft': 19,
        'v/s ft/min': 29,
        'vel kts': 44,
        'hdg': 53,
        'lat': 58,
        'lon': 68
    })

    __data_key_dict = OrderedDict({
        'call_sign': {'offset': 8, 'display': lambda x: x},
        'altitude': {'offset': 19, 'display': lambda x: x},
        'vs': {'offset': 29, 'display': lambda x: x},
        'velocity': {'offset': 44, 'display': lambda x: int(x)},
        'heading': {'offset': 53, 'display': lambda x: int(x)},
        'latitude': {'offset': 58, 'display': lambda x: "{:.8s}".format(str(x))},
        'longitude': {'offset': 68, 'display': lambda x: "{:.8s}".format(str(x))}
    })

    @staticmethod
    def curses_table_output(global_aircraft_dict):
        """
        Output aircraft dictionary in table format
        """
        stdscr = curses.initscr()
        curses.noecho()

        if stdscr.getmaxyx()[1] < 80:
            stdscr.addstr("Terminal must be at least 80 characters wide")
            return

        # Print the table header
        stdscr.clear()
        for key in Output.__header_dict:
            stdscr.addstr(0, Output.__header_dict[key], key)

        # Print aircraft data to table
        y = 1
        for icao in global_aircraft_dict:
            stdscr.addstr(y, 0, icao)

            for key in Output.__data_key_dict:
                if key in global_aircraft_dict[icao]:
                    stdscr.addstr(y, Output.__data_key_dict[key]['offset'],
                                  str(Output.__data_key_dict[key]['display'](global_aircraft_dict[icao][key])))
            y += 1

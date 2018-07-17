import curses


class Output:
    __global_aircraft_dict = {}

    @staticmethod
    def curses_table_output(global_aircraft_dict):
        Output.__global_aircraft_dict = global_aircraft_dict
        curses.wrapper(Output.__curses_table_output)

    @staticmethod
    def __curses_table_output(stdscr):
        """
        Output aircraft dictionary in table format
        """
        if stdscr.getmaxyx()[1] < 80:
            stdscr.addstr("Terminal must be at least 80 characters wide")
            return

        # TODO: make these ordered dicts
        header_dict = {
            'ICAO': 0,
            'Call Sign': 8,
            'Alt ft': 19,
            'v/s ft/min': 29,
            'vel kts': 44,
            'hdg': 53,
            'lat': 58,
            'lon': 66
        }
        header_order = ['ICAO', 'Call Sign', 'Alt ft', 'v/s ft/min', 'vel kts', 'hdg', 'lat', 'lon']

        data_key_dict = {
            'call_sign': 8,
            'altitude': 19,
            'vs': 29,
            'velocity': 44,
            'heading': 53,
            'latitude': 58,
            'longitude': 66
        }
        data_key_order = ['call_sign', 'altitude', 'vs', 'velocity', 'heading', 'latitude', 'longitude']

        # Print the table header
        stdscr.clear()
        for key in header_order:
            stdscr.addstr(0, header_dict[key], key)

        # Print aircraft data to table
        y = 1
        for icao in Output.__global_aircraft_dict:
            stdscr.addstr(y, 0, icao)

            for key in data_key_order:
                stdscr.addstr(y, data_key_dict[key], Output.__global_aircraft_dict[key])

            y += 1

        stdscr.getch()


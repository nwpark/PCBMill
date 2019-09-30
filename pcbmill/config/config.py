from enum import IntEnum

data_bus_pins = [5, 6, 13, 19, 26, 16, 20, 21]
cmd_bus_pins = [9, 11, 25, 8]
req_pin = 17
ack_pin = 4

ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Command(IntEnum):
    LOAD_DATA = 0
    GOTO = 1

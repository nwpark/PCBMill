from bitstring import BitArray
from pcbmill.common.utils import convert_to_iterable
from pcbmill.config.config import *

OUT = 0
IN = 1
PUD_DOWN = 2
RISING = 3
FALLING = 4
BCM = 5


mock_pins = dict()
pin_callbacks = list()


# Helper methods for tests

def add_conditional_pin_callback(pins, callback):
    pins = convert_to_iterable(pins)
    pin_callbacks.append((pins, callback))


def update_mock_pins(pins, values):
    pins = convert_to_iterable(pins)
    values = convert_to_iterable(values)
    mock_pins.update(zip(pins, values))

    for conditional_callback in pin_callbacks:
        conditional_pins = conditional_callback[0]
        callback = conditional_callback[1]
        if set(conditional_pins).issubset(pins):
            callback()


def read_pin_value(pin):
    return mock_pins.get(pin)


def read_bus_value(bus_pins):
    bit_str = ''.join([str(mock_pins.get(pin)) for pin in bus_pins])
    return BitArray(bin=bit_str).int


# Core GPIO methods

def setmode(mode):
    pass


def setup(pin, mode, initial=None, pull_up_down=None):
    mock_pins.update({pin:  0})


def output(pins, values):
    update_mock_pins(pins, values)


def input(pin):
    return mock_pins.get(pin)


def wait_for_edge(pin, edge):
    if edge == RISING:
        expected = 1
    else:
        expected = 0
    while mock_pins.get(pin) != expected:
        pass
    return


def cleanup():
    pass


# Helper methods

def print_mock_pins():
    def format_mock_bus(bus_pins):
        bus_status = ''
        for pin in bus_pins:
            bus_status += str(mock_pins.get(pin))
        return bus_status
    pin_status = 'Data bus: {}'.format(format_mock_bus(data_bus_pins))
    pin_status += ', cmd bus: {}'.format(format_mock_bus(cmd_bus_pins))
    pin_status += ', req: {}'.format(mock_pins.get(req_pin))
    pin_status += ', ack: {}'.format(mock_pins.get(ack_pin))
    print(pin_status)

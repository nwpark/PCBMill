from pcbmill.config.config import *

OUT = 0
IN = 1
PUD_DOWN = 2
RISING = 3
FALLING = 4


mock_pins = dict()
mock_pin_callbacks = list()


def add_mock_pin_callback(callback):
    mock_pin_callbacks.append(callback)


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


def update_mock_pins(pins, values):
    if not hasattr(pins, '__iter__'):
        pins = [pins]
    if not hasattr(values, '__iter__'):
        values = [values]
    for pin, value in zip(pins, values):
        mock_pins[pin] = value
    for callback in mock_pin_callbacks:
        callback(pins, values)


def output(pins, values):
    update_mock_pins(pins, values)


def setup(pin, mode, pull_up_down=None):
    mock_pins[pin] = 0


def wait_for_edge(pin, edge):
    if edge == RISING:
        target = 1
    else:
        target = 0
    while mock_pins.get(pin) != target:
        pass
    return


def input(pin):
    return mock_pins.get(pin)

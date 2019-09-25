from pcbmill.config.config import data_bus_pins, cmd_bus_pins, req_pin, ack_pin

mock_pins = dict()
mock_pin_callbacks = list()


def format_bus_values(bus_pins):
    bus_status = ''
    for pin in bus_pins:
        bus_status += str(mock_pins.get(pin, 0))
    return bus_status


def print_mock_pins():
    pin_status = 'Data bus: {}'.format(format_bus_values(data_bus_pins))
    pin_status += ', cmd bus: {}'.format(format_bus_values(cmd_bus_pins))
    pin_status += ', req: {}'.format(mock_pins.get(req_pin, 0))
    pin_status += ', ack: {}'.format(mock_pins.get(ack_pin, 0))
    print(pin_status)


def update_mock_pin(pin, value):
    mock_pins[pin] = value
    if pin == req_pin or pin == ack_pin:
        print_mock_pins()
    for callback in mock_pin_callbacks:
        callback(pin, value)


class DigitalOutputDevice:
    def __init__(self, pin):
        self.pin = pin
        self.value = 0

    def update_global_state(self):
        update_mock_pin(self.pin, self.value)

    def on(self):
        self.value = 1
        self.update_global_state()

    def off(self):
        self.value = 0
        self.update_global_state()

    def toggle(self):
        self.value = (self.value + 1) % 2
        self.update_global_state()

    def __str__(self):
        return "pin=%d val=%d" % (self.pin, self.value)

    def __repr__(self):
        return self.__str__()


class DigitalInputDevice:
    def __init__(self, pin):
        self.pin = pin
        self.value = 0

    def wait_for_active(self):
        # while mock_pins[self.pin] != 1:
        while mock_pins.get(self.pin, 0) != 1:
            pass
        return

    def wait_for_inactive(self):
        # while mock_pins[self.pin] != 0:
        while mock_pins.get(self.pin, 0) != 0:
            pass
        return

    def __str__(self):
        return "pin=%d val=%d" % (self.pin, self.value)

    def __repr__(self):
        return self.__str__()

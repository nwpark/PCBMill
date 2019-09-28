from concurrent.futures import ThreadPoolExecutor
from pcbmill.config.config import data_bus_pins, cmd_bus_pins, req_pin, ack_pin
from pcbmill.server.gpio import DigitalOutputPin, DigitalInputPin, DigitalOutputBus


class FPGAInterface:
    def __init__(self):
        self.data_bus = DigitalOutputBus(data_bus_pins)
        self.cmd_bus = DigitalOutputBus(cmd_bus_pins)
        self.req_pin = DigitalOutputPin(req_pin)
        self.ack_pin = DigitalInputPin(ack_pin)

    def set_data(self, data):
        self.data_bus.write(data)

    def request_action(self, cmd):
        assert self.req_pin.value() == 0
        self.ack_pin.wait_for_inactive()
        self.cmd_bus.write(cmd)
        self.req_pin.on()
        return ThreadPoolExecutor().submit(self.__wait_for_ack)

    def __wait_for_ack(self):
        self.ack_pin.wait_for_active()
        self.req_pin.off()

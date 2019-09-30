from concurrent.futures import ThreadPoolExecutor
from pcbmill.config.config import data_bus_pins, cmd_bus_pins, req_pin, ack_pin
from pcbmill.server.gpio import DigitalOutputPin, DigitalInputPin, DigitalOutputBus
from RPi import GPIO
import logging


class FPGAInterface:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.data_bus = DigitalOutputBus(data_bus_pins)
        self.cmd_bus = DigitalOutputBus(cmd_bus_pins)
        self.req_pin = DigitalOutputPin(req_pin)
        self.ack_pin = DigitalInputPin(ack_pin)
        self._log = logging.getLogger(__name__)

    def request_action(self, cmd, data):
        self._log.info("Requested action '{}' with data '{}'.".format(cmd, data))
        assert self.req_pin.value() == 0
        assert self.ack_pin.value() == 0

        if data is not None:
            self.data_bus.write(data)

        self.cmd_bus.write(cmd)

        self.req_pin.on()
        return ThreadPoolExecutor().submit(self.__wait_for_ack)

    def cleanup(self):
        GPIO.cleanup()

    def __wait_for_ack(self):
        self.ack_pin.wait_for_active()
        self._log.info('Acknowledgement received.')

        self.req_pin.off()
        self.ack_pin.wait_for_inactive()

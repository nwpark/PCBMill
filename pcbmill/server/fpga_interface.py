from concurrent.futures import ThreadPoolExecutor
from pcbmill.config.config import data_bus_pins, cmd_bus_pins, req_pin, ack_pin
from pcbmill.generated.cnc_mill_pb2 import Command
from pcbmill.server.gpio import DigitalOutputPin, DigitalInputPin, DigitalOutputBus
from RPi import GPIO
import logging


class FPGAInterface:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self._data_bus = DigitalOutputBus(data_bus_pins)
        self._cmd_bus = DigitalOutputBus(cmd_bus_pins)
        self._req_pin = DigitalOutputPin(req_pin)
        self._ack_pin = DigitalInputPin(ack_pin)
        self._log = logging.getLogger(__name__)

    def request_action(self, cmd, data=None):
        self._log.info("Requested action {} (enum value={}) with data={}.".format(Command.Name(cmd), cmd, data))
        assert self._req_pin.value() == 0, 'Request was made but req was already high.'
        assert self._ack_pin.value() == 0, 'Request was made but ack was already high.'

        if data is not None:
            self._data_bus.write(data)

        self._cmd_bus.write(cmd)

        self._req_pin.on()
        return ThreadPoolExecutor().submit(self._wait_for_ack)

    def cleanup(self):
        self._log.info('Cleaning up GPIO.')
        GPIO.cleanup()

    def _wait_for_ack(self):
        self._log.info('Waiting for ack...')
        self._ack_pin.wait_for_active()
        self._log.info('Ack received.')

        self._req_pin.off()
        self._ack_pin.wait_for_inactive()

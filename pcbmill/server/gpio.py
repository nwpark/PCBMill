from pcbmill.common.utils import convert_to_bit_array
from RPi import GPIO
import logging


class DigitalOutputBus:
    def __init__(self, bus_pins):
        self._bus_pins = bus_pins
        for pin in bus_pins:
            GPIO.setup(pin, GPIO.OUT, initial=0)

    def write(self, data):
        bit_array = convert_to_bit_array(data, len(self._bus_pins))
        GPIO.output(self._bus_pins, bit_array)


class DigitalPin:
    def __init__(self, pin):
        self._pin = pin
        self._log = logging.getLogger(__name__)
        GPIO.add_event_detect(pin, GPIO.BOTH, callback=self._log_event)

    def value(self):
        return GPIO.input(self._pin)

    def _log_event(self, channel):
        self._log.info('Event detected on channel {}. Value = {}.'.format(channel, GPIO.input(channel)))


class DigitalOutputPin(DigitalPin):
    def __init__(self, pin):
        super().__init__(pin)
        GPIO.setup(pin, GPIO.OUT, initial=0)

    def on(self):
        GPIO.output(self._pin, 1)

    def off(self):
        GPIO.output(self._pin, 0)


class DigitalInputPin(DigitalPin):
    def __init__(self, pin):
        super().__init__(pin)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def wait_for_active(self):
        # if self.value() != 1:
        #     GPIO.wait_for_edge(self._pin, GPIO.RISING)
        while self.value() != 1:
            pass

    def wait_for_inactive(self):
        # if self.value() != 0:
        #     GPIO.wait_for_edge(self._pin, GPIO.FALLING)
        while self.value() != 0:
            pass

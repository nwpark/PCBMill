from pcbmill.common.utils import convert_to_bit_array
from RPi import GPIO
import logging


class DigitalOutputBus:
    def __init__(self, bus_pins):
        self.bus_pins = bus_pins
        for pin in bus_pins:
            GPIO.setup(pin, GPIO.OUT)

    def write(self, data):
        bit_array = convert_to_bit_array(data, len(self.bus_pins))
        GPIO.output(self.bus_pins, bit_array)


class DigitalPin:
    def __init__(self, pin):
        self.pin = pin
        self._log = logging.getLogger('pin_{}'.format(pin))

    def value(self):
        return GPIO.input(self.pin)


class DigitalOutputPin(DigitalPin):
    def __init__(self, pin):
        super().__init__(pin)
        GPIO.setup(pin, GPIO.OUT)

    def on(self):
        self._log.info('Output set high')
        GPIO.output(self.pin, 1)

    def off(self):
        self._log.info('Output set low')
        GPIO.output(self.pin, 0)


class DigitalInputPin(DigitalPin):
    def __init__(self, pin):
        super().__init__(pin)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def wait_for_active(self):
        if self.value() != 1:
            GPIO.wait_for_edge(self.pin, GPIO.RISING)

    def wait_for_inactive(self):
        if self.value() != 0:
            GPIO.wait_for_edge(self.pin, GPIO.FALLING)

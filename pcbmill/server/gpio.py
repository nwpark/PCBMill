from RPi import GPIO


class DigitalOutputBus:
    def __init__(self, bus_pins):
        self.bus_pins = bus_pins
        for pin in bus_pins:
            GPIO.setup(pin, GPIO.OUT)

    def write(self, data):
        bin_str = bin(5)[2:]
        bin_str = '{:0>8}'.format(bin_str)
        bit_array = list(map(lambda i: int(i), list(bin_str)))
        GPIO.output(self.bus_pins, bit_array)


class DigitalPin:
    def __init__(self, pin):
        self.pin = pin

    def value(self):
        return GPIO.input(self.pin)


class DigitalOutputPin(DigitalPin):
    def __init__(self, pin):
        super().__init__(pin)
        GPIO.setup(pin, GPIO.OUT)

    def on(self):
        GPIO.output(self.pin, 1)

    def off(self):
        GPIO.output(self.pin, 0)


class DigitalInputPin(DigitalPin):
    def __init__(self, pin):
        super().__init__(pin)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def wait_for_active(self):
        GPIO.wait_for_edge(self.pin, GPIO.RISING)

    def wait_for_inactive(self):
        GPIO.wait_for_edge(self.pin, GPIO.FALLING)

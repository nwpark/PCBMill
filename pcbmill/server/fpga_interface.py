from gpiozero import DigitalOutputDevice, DigitalInputDevice
from concurrent.futures import ThreadPoolExecutor
from pcbmill.config.config import data_bus_pins, cmd_bus_pins, req_pin, ack_pin


class OutputBus:
    def __init__(self, bus_pins):
        self.bus = list(map(lambda i: DigitalOutputDevice(i), bus_pins))

    def set_value(self, data):
        for index, output_device in enumerate(self.bus):
            if (data >> index) & 1 != output_device.value:
                output_device.toggle()


class FPGAInterface:
    def __init__(self):
        self.data_bus = OutputBus(data_bus_pins)
        self.cmd_bus = OutputBus(cmd_bus_pins)
        self.req_pin = DigitalOutputDevice(req_pin)
        self.ack_pin = DigitalInputDevice(ack_pin)

    def set_data(self, data):
        self.data_bus.set_value(data)

    def request_action(self, cmd):
        assert self.req_pin.value == 0
        self.ack_pin.wait_for_inactive()
        self.cmd_bus.set_value(cmd)
        self.req_pin.on()
        return ThreadPoolExecutor().submit(self.__wait_for_ack)

    def __wait_for_ack(self):
        self.ack_pin.wait_for_active()
        self.req_pin.off()


if __name__ == '__main__':
    fpga_interface = FPGAInterface()

    fpga_interface.set_data(1)

    future = fpga_interface.request_action(1)
    future.add_done_callback(lambda i: print(i))

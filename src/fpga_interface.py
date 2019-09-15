from gpiozero import DigitalOutputDevice

#    3V3  (1) (2)  5V
#  GPIO2  (3) (4)  5V
#  GPIO3  (5) (6)  GND
#  GPIO4  (7) (8)  GPIO14
#    GND  (9) (10) GPIO15
# GPIO17 (11) (12) GPIO18
# GPIO27 (13) (14) GND
# GPIO22 (15) (16) GPIO23
#    3V3 (17) (18) GPIO24
# GPIO10 (19) (20) GND
#  GPIO9 (21) (22) GPIO25
# GPIO11 (23) (24) GPIO8
#    GND (25) (26) GPIO7
#  GPIO0 (27) (28) GPIO1
#  GPIO5 (29) (30) GND
#  GPIO6 (31) (32) GPIO12
# GPIO13 (33) (34) GND
# GPIO19 (35) (36) GPIO16
# GPIO26 (37) (38) GPIO20
#    GND (39) (40) GPIO21

data_bus_pins = [5, 6, 13, 19, 26, 16, 20, 21]
cmd_bus_pins = [9, 11, 25, 8]
req_pin = 2
ack_pin = 3


class Bus:
    def __init__(self, bus_pins):
        self.bus = map(lambda i: DigitalOutputDevice(i), bus_pins)

    def write(self, data):
        for index, output_device in enumerate(self.bus):
            if data & (1 << index):
                output_device.on()
            else:
                output_device.off()


if __name__ == '__main__':
    data_bus = Bus(data_bus_pins)
    cmd_bus = Bus(cmd_bus_pins)

    data_bus.write(1)
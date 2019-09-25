import gpio_mock as gpio__mock
import sys
sys.modules['gpiozero'] = gpio__mock

from pcbmill.config.config import *
from gpio_mock import mock_pins, mock_pin_callbacks, update_mock_pin
from pcbmill.server import cnc_mill_server
from pcbmill.server.fpga_interface import req_pin, ack_pin


def req_callback(pin, value):
    if pin == req_pin and value == 1:
        update_mock_pin(ack_pin, 1)
    if pin == req_pin and value == 0:
        update_mock_pin(ack_pin, 0)


for pin in data_bus_pins + cmd_bus_pins:
    mock_pins[pin] = 0

mock_pin_callbacks.append(req_callback)

cnc_mill_server.serve()

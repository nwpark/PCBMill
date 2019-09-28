from pcbmill.config.config import req_pin, ack_pin
from pcbmill.tests.mock_rpi.GPIO import print_mock_pins, update_mock_pins, add_mock_pin_callback
from pcbmill.generated.cnc_mill_pb2 import Position
import sys
import pcbmill.tests.mock_rpi as mock__rpi
sys.modules['RPi'] = mock__rpi
from pcbmill.server import cnc_mill_server


def callback(pins, values):
    if pins == [req_pin] or pins == [ack_pin]:
        print_mock_pins()
    if pins == [req_pin]:
        update_mock_pins(ack_pin, values)


add_mock_pin_callback(callback)

servicer = cnc_mill_server.CNCMillServicer()
servicer.GoTo(Position(x=5, y=7), None)

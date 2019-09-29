import unittest
from pcbmill.config.config import req_pin, ack_pin, data_bus_pins, cmd_bus_pins, Command
from pcbmill.tests.mock_rpi.GPIO import mock_pins, update_mock_pins, pin_callbacks, add_conditional_pin_callback, read_pin_value, read_bus_value
from pcbmill.generated.cnc_mill_pb2 import Position
import sys
import pcbmill.tests.mock_rpi as mock__rpi
sys.modules['RPi'] = mock__rpi
from pcbmill.server.cnc_mill_server import CNCMillServicer


class TestCNCMillServicer(unittest.TestCase):

    def setUp(self):
        self.cnc_mill_servicer = CNCMillServicer()
        pin_callbacks.clear()
        self.actual_requests = list()
        add_conditional_pin_callback(req_pin, self.assert_valid_req)
        add_conditional_pin_callback(ack_pin, self.assert_valid_ack)
        add_conditional_pin_callback(req_pin, self.record_request)
        add_conditional_pin_callback(req_pin, self.respond_to_req)

    def respond_to_req(self):
        req_pin_val = read_pin_value(req_pin)
        update_mock_pins(ack_pin, req_pin_val)

    def assert_valid_req(self):
        req_pin_val = read_pin_value(req_pin)
        self.assertEqual(read_pin_value(ack_pin), (req_pin_val + 1) % 2)

    def assert_valid_ack(self):
        ack_pin_val = read_pin_value(ack_pin)
        self.assertEqual(read_pin_value(req_pin), ack_pin_val)

    def record_request(self):
        if read_pin_value(req_pin) == 1:
            cmd = read_bus_value(cmd_bus_pins)
            data = read_bus_value(data_bus_pins)
            self.actual_requests.append((cmd, data))

    def test_goto(self):
        target = Position(x=1, y=2)
        expected_requests = [(Command.LOAD_DATA, 1), (Command.LOAD_DATA, 2), (Command.GOTO, 2)]

        self.cnc_mill_servicer.GoTo(target, None)

        self.assertEqual(self.actual_requests, expected_requests)

    def test_goto_2(self):
        target = Position(x=3, y=7)
        expected_requests = [(Command.LOAD_DATA, 3), (Command.LOAD_DATA, 7), (Command.GOTO, 7)]

        self.cnc_mill_servicer.GoTo(target, None)

        self.assertEqual(self.actual_requests, expected_requests)


if __name__ == '__main__':
    unittest.main()

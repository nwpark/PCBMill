from pcbmill.config.config import req_pin, ack_pin, data_bus_pins, cmd_bus_pins, log_format, log_datefmt
from pcbmill.generated.cnc_mill_pb2 import Position, Command
from pcbmill.tests.server.mock_rpi.GPIO import update_mock_pins, pin_callbacks, add_conditional_pin_callback, read_pin_value, read_bus_value
import logging
import pcbmill.tests.server.mock_rpi as mock__rpi
import sys
import unittest
sys.modules['RPi'] = mock__rpi
from pcbmill.server.cnc_mill_server import CNCMillServicer


class TestCNCMillServicer(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.INFO, format=log_format, datefmt=log_datefmt)
        self.cnc_mill_servicer = CNCMillServicer()
        pin_callbacks.clear()
        self.recorded_requests = list()
        add_conditional_pin_callback(req_pin, self.assert_valid_req)
        add_conditional_pin_callback(ack_pin, self.assert_valid_ack)
        add_conditional_pin_callback(req_pin, self.record_request)
        add_conditional_pin_callback(req_pin, self.respond_to_req)

    def respond_to_req(self):
        req_pin_val = read_pin_value(req_pin)
        update_mock_pins(ack_pin, req_pin_val)

    def assert_valid_req(self):
        req_pin_val = read_pin_value(req_pin)
        expected_ack_val = int(not req_pin_val)
        self.assertEqual(expected_ack_val, read_pin_value(ack_pin))

    def assert_valid_ack(self):
        expected_req_val = read_pin_value(ack_pin)
        self.assertEqual(expected_req_val, read_pin_value(req_pin))

    def record_request(self):
        if read_pin_value(req_pin) == 1:
            cmd = read_bus_value(cmd_bus_pins)
            data = read_bus_value(data_bus_pins)
            self.recorded_requests.append((cmd, data))

    def test_goto(self):
        target = Position(x=1, y=2, z=3)
        expected_requests = [
            (Command.LOAD_DATA, 1),
            (Command.LOAD_DATA, 0),
            (Command.LOAD_DATA, 0),
            (Command.LOAD_DATA, 0),
            (Command.LOAD_DATA, 2),
            (Command.LOAD_DATA, 0),
            (Command.LOAD_DATA, 0),
            (Command.LOAD_DATA, 0),
            (Command.LOAD_DATA, 3),
            (Command.LOAD_DATA, 0),
            (Command.LOAD_DATA, 0),
            (Command.LOAD_DATA, 0),
            (Command.GOTO, 0)
        ]

        self.cnc_mill_servicer.GoTo(target, None)
        self.assertEqual(expected_requests, self.recorded_requests)

    def test_goto_2(self):
        target = Position(x=3, y=7, z=5)
        expected_requests = [
            (Command.LOAD_DATA, 3),
            (Command.LOAD_DATA, 0),
            (Command.LOAD_DATA, 0),
            (Command.LOAD_DATA, 0),
            (Command.LOAD_DATA, 7),
            (Command.LOAD_DATA, 0),
            (Command.LOAD_DATA, 0),
            (Command.LOAD_DATA, 0),
            (Command.LOAD_DATA, 5),
            (Command.LOAD_DATA, 0),
            (Command.LOAD_DATA, 0),
            (Command.LOAD_DATA, 0),
            (Command.GOTO, 0)
        ]

        self.cnc_mill_servicer.GoTo(target, None)
        self.assertEqual(expected_requests, self.recorded_requests)


if __name__ == '__main__':
    unittest.main()

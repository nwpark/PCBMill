import unittest
from unittest.mock import MagicMock
from unittest.mock import call
from pcbmill.grpc.cnc_mill_pb2 import Position
from pcbmill.server.cnc_mill_server import CNCMillServicer


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.servicer = CNCMillServicer()
        self.servicer.fpga = MagicMock()

    def test_goto(self):
        position = Position()
        position.x = 1
        position.y = 2
        self.servicer.GoTo(position, None)
        self.servicer.fpga.set_data.assert_has_calls([call(1), call(2)])
        self.servicer.fpga.request_action.assert_has_calls([call(0), call().result(), call(0), call().result(), call(1), call().result()])


if __name__ == '__main__':
    unittest.main()

import unittest
from pathlib import Path

from gate import FeigResponse, FeigRequest
from gate.request import PeopleCounterRequest
from gate.response import PeopleCounterResponse

test_data = Path('test_data')


class TestCounterData(unittest.TestCase):
    def test_response_no_request_isostart(self):
        data = test_data.joinpath('response_counter_data_isostart.txt').read_bytes()
        response_obj = FeigResponse.parse_response(data)
        self.assertEqual(443631, response_obj.people_in)
        self.assertEqual(447560, response_obj.people_out)


    def test_response_no_request_rfid(self):
        data = test_data.joinpath('response_counter_data_rfid.txt').read_bytes()
        response_obj = FeigResponse.parse_response(data)
        self.assertEqual(443672, response_obj.people_in)
        self.assertEqual(447584, response_obj.people_out)

    def test_response_and_request(self):
        request = test_data.joinpath('request_1765060339.txt').read_bytes()
        response = test_data.joinpath('response_1765060339.txt').read_bytes()
        request_obj = FeigRequest.parse_request(request)
        self.assertIsInstance(request_obj, PeopleCounterRequest)

        response_obj = request_obj.parse_response(response)
        self.assertIsInstance(response_obj, PeopleCounterResponse)
        self.assertEqual(443749, response_obj.people_in)
        self.assertEqual(447674, response_obj.people_out)
        pass

    def test_response_no_request2(self):
        data = test_data.joinpath('response_1765060339.txt').read_bytes()
        response_obj = FeigResponse.parse_response(data)
        self.assertEqual(443749, response_obj.people_in)
        self.assertEqual(447674, response_obj.people_out)
        pass

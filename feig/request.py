from feig.response import FeigResponse


def parse_header(request: bytes):
    length = request[0]
    if request[1] == 0xff:
        command = request[2]
        payload = request[4:]
        data_format = 'isostart'
    elif request[3] == 0xff:
        length = request[2]
        command = request[4]
        payload = request[5:]
        data_format = 'isostart_advanced'
    else:
        data_format = 'rfidif'
        command = request[2]
        payload = request[3:]
    return command, length, payload, data_format


class FeigRequest:
    mode: int = None

    def __init__(self, request: bytes):
        self.data = request
        self.command, self.length, self.payload, self.format = parse_header(request)

    @staticmethod
    def parse_request(request: bytes) -> 'FeigRequest':
        command, length, payload, data_format = parse_header(request)
        if command in request_classes:
            return request_classes[command](request)
        else:
            return FeigRequest(request)

    def parse_response(self, response: bytes) -> FeigResponse:
        return FeigResponse.parse_response(response, self.command, self)


class ReadBufferRequest(FeigRequest):
    pass


class ClearBufferRequest(FeigRequest):
    pass


class ReaderInfoRequest(FeigRequest):
    mode: int

    def __init__(self, request: bytes):
        super().__init__(request)
        self.mode = self.payload[0]


class PeopleCounterRequest(FeigRequest):
    def __init__(self, request: bytes):
        super().__init__(request)
        if self.format == 'rfidif':
            self.mode = self.payload[5]
        elif self.format in ['isostart', 'isostart_advanced']:
            self.mode = self.payload[7]
        else:
            raise RuntimeError('Unknown format')
        self.property1 = self.payload[3]


request_classes = {
    0x22: ReadBufferRequest,
    0x32: ClearBufferRequest,
    0x66: ReaderInfoRequest,
    0x9f: PeopleCounterRequest,
}

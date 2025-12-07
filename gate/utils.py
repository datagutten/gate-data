def hex_string(data: bytes):
    string = ''
    for octet in data:
        # octet = ord(octet)
        if octet <= 0x0f:
            string += '0'
        # Format as lower case hex digit without prefix
        string += format(octet, 'x') + ' '
    return string


def format_ip(data: bytes):
    if data is None:
        return None
    ip = ''
    for byte in data:
        ip += '%d.' % byte
    return ip[:-1]

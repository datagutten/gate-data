import flask
from flask import Flask

from .gate_socket import FeigGate

app = Flask(__name__)

connections = {}


def get_connection(gate_id=None):
    if gate_id is None:
        gate_id = flask.request.args.get('gate')
    if gate_id not in connections:
        gate_obj = FeigGate(gate_id)
        connections[gate_id] = gate_obj
    else:
        gate_obj = connections[gate_id]

    gate_obj.save = True

    return gate_obj


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/people')
def count():
    gate_obj = get_connection(flask.request.args.get('gate'))
    counter = gate_obj.people_count()
    return {'in': counter.people_in, 'out': counter.people_out, 'raw': counter.base64()}


@app.route('/info')
def info():
    gate_obj = get_connection()
    info_obj = gate_obj.gate_info
    return {
        'hardware_type': info_obj.hardware_type,
        'serial': info_obj.id,
        'ip': info_obj.ip,
        'netmask': info_obj.netmask,
        'gateway': info_obj.gateway,
        'mac': info_obj.mac,
        'peripheral_count': info_obj.peripheral_count,
        'reader_type': info_obj.reader_type,
        'rx_buffer': info_obj.rx_buffer,
        'tx_buffer': info_obj.tx_buffer,
        'status': info_obj.status,
        'transponder_types': info_obj.transponder_types,
        'version': info_obj.version,
        'raw': info_obj.base64(),
    }


@app.route('/buffer')
def buffer():
    gate_obj = get_connection()
    buffer_data = gate_obj.read_buffer()

    if not buffer_data.success:
        return {'raw': buffer_data.base64()}
    tags = buffer_data.tags()
    return {
        'tags': tags,
        'raw': buffer_data.base64()
    }


@app.route('/raw', methods=["POST"])
def raw():
    gate_obj = get_connection()
    data = flask.request.data
    response = gate_obj.send_read(data)
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0')

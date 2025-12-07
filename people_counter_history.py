import datetime
import re
from pathlib import Path

from prometheus_client.openmetrics.exposition import generate_latest

from gate import FeigResponse
from metrics import people, registry

data_path = Path('data')
lines = None
samples = {}
samples_time = {}
for gate in data_path.iterdir():
    if not gate.is_dir():
        continue
    samples[gate.stem] = {}
    print(gate)
    for file in gate.iterdir():
        if file.is_dir():
            continue

        data = file.read_bytes()
        if len(data) == 0:
            file.unlink()
            continue
        if 'response' in file.stem:
            try:
                response_obj = FeigResponse.parse_response(data)
            except RuntimeError as e:
                # print(e)
                continue
            if response_obj.command == 0x9f:
                timestamp = re.sub(r'.+_(\d+)\.txt', r'\1', file.name)
                timestamp = int(timestamp)
                date_obj = datetime.datetime.fromtimestamp(int(timestamp))
                if not hasattr(response_obj, 'people_in'):
                    print('People count not found in %s' % file)
                    continue
                samples[gate.stem][timestamp] = {'in': response_obj.people_in, 'out': response_obj.people_out}
                sample = {'in': response_obj.people_in, 'out': response_obj.people_out, 'gate': gate.stem}
                if timestamp not in samples_time:
                    samples_time[timestamp] = [sample]
                else:
                    samples_time[timestamp].append(sample)

timestamps = list(samples_time.keys())
timestamps.sort()
print(datetime.datetime.fromtimestamp(timestamps[0]).isoformat(), timestamps[0])
print(datetime.datetime.fromtimestamp(timestamps[-1]).isoformat(), timestamps[-1])

for timestamp in timestamps:
    for sample in samples_time[timestamp]:
        people.labels('in', sample['gate'], 1).set(sample['in'])
        people.labels('out', sample['gate'], 1).set(sample['out'])

        data = generate_latest(registry)
        if lines is None:
            lines = data.splitlines()[0:2]
        else:
            lines_temp = data.splitlines()[2:-1]
            for line in lines_temp:
                lines.append(b'%s %s' % (line, str(timestamp).encode()))

lines.append(b'# EOF')
Path('metrics.txt').write_bytes(b'\n'.join(lines))

pass

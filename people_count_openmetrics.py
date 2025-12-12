import json
import os
from datetime import datetime
from pathlib import Path

from prometheus_client import generate_latest

from metrics import people, registry

output_folder = Path(os.getenv('METRICS_FOLDER'))
output_folder.mkdir(parents=True, exist_ok=True)

lines = None
path = Path('parsed_data')
for gate in path.iterdir():
    if not gate.is_dir():
        continue

    for date in gate.iterdir():
        if not date.is_dir():
            continue
        file = date.joinpath('PeopleCounterResponse.json')
        if not file.exists():
            continue
        print(file)
        with file.open() as fp:
            data = json.load(fp)
            data = {k: v for k, v in sorted(list(data.items()))}

            for timestamp, tags in data.items():
                date_obj = datetime.fromtimestamp(int(timestamp))
                people.labels('in', gate.name, 1).set(tags['in'])
                people.labels('out', gate.name, 1).set(tags['out'])

                data = generate_latest(registry)
                if lines is None:
                    lines = data.splitlines()[0:2]
                else:
                    lines_temp = data.splitlines()[2:-1]
                    for line in lines_temp:
                        lines.append(b'%s %s' % (line, str(timestamp).encode()))

    lines.append(b'# EOF')
    output_file = output_folder.joinpath('metrics_%s.txt' % gate.name)
    output_file.write_bytes(b'\n'.join(lines))
    print(output_file)
    lines = None

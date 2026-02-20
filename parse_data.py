# Sort data files by date
# Extract relevant data to json
# gzip files as backup
import datetime
import json
import subprocess
import sys
from pathlib import Path

from feig import gate_data

output_folder = Path('parsed_data')
data_folder = Path(sys.argv[1])
date_files = gate_data.sort_files(data_folder)
for gate, dates in date_files.items():
    for date, files in dates.items():
        print(gate, date)
        output = {}

        date_folder = output_folder.joinpath(gate, date.isoformat())
        date_folder.mkdir(parents=True, exist_ok=True)
        for file in files:
            timestamp = gate_data.get_file_timestamp(file)
            try:
                response_obj = gate_data.get_conversation(file)
            except RuntimeError as e:
                print(e)
                continue
            except IndexError as e:
                print(e)
                continue
            if not response_obj:
                continue

            name = type(response_obj).__name__
            if name not in output:
                output[name] = {}
            try:
                data = response_obj.dict()
                if data:
                    output[name][timestamp] = data
            except NotImplementedError:
                continue
            except RuntimeError as e:
                print(e)
                continue

        for class_name, values in output.items():
            if not values:
                continue
            with date_folder.joinpath(class_name).with_suffix('.json').open('w') as fp:
                json.dump(values, fp)

        if date != datetime.date.today():
            gate_folder_input = data_folder.joinpath(gate)
            archive_path = data_folder.joinpath('%s_%s.tar.gz' % (date.isoformat(), gate)).resolve()
            cmd = ['tar', '-cvzf', str(archive_path), '--remove-files',
                   date.isoformat()]
            process = subprocess.run(cmd, cwd=gate_folder_input)
            process.check_returncode()
            pass

# Unpack tar.gz files created by parse_data.py and recreate original directory structure

import re
import subprocess
import sys
from pathlib import Path


def unpack_tars(tar_path: Path, output_folder: Path):
    output_folder.mkdir(exist_ok=True)
    for file in tar_path.iterdir():
        if not file.is_file() or not file.name.endswith('.tar.gz'):
            continue
        date, gate = re.search(r'(\d{4}-\d{2}-\d{2})_(\d+).tar.gz', file.name).groups()
        gate_folder = output_folder.joinpath(gate)
        gate_folder.mkdir(exist_ok=True)

        subprocess.run(['tar', '-xzf', str(file), '-C', str(gate_folder)])


if __name__ == '__main__':
    unpack_tars(Path(sys.argv[1]), Path(sys.argv[2]))

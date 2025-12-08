import datetime
import re
from pathlib import Path
from typing import Tuple, Optional

from gate import FeigRequest, FeigResponse


def get_file_timestamp(file: Path) -> int:
    return int(re.sub(r'.+_(\d+)\.txt', r'\1', file.name))


def get_file_date(file: Path) -> datetime.date:
    timestamp = int(re.sub(r'.+_(\d+)\.txt', r'\1', file.name))
    return datetime.date.fromtimestamp(timestamp)


def sort_files(path: Path) -> dict[str, dict[datetime.date, list[Path]]]:
    """
    Sort files in folders by date
    :param path:
    :return:
    """
    date_files_all = {}
    for gate in path.iterdir():
        date_files = {}
        if not gate.is_dir():
            continue
        for file in gate.iterdir():
            if file.is_dir():
                try:
                    date = datetime.date.fromisoformat(file.name)
                    date_files[date] = list(file.iterdir())
                    continue
                except ValueError:
                    continue

            if not file.is_file() or file.suffix != '.txt':
                continue
            date = get_file_date(file)
            if date not in date_files:
                date_files[date] = []
            if date == datetime.date.today():
                date_files[date].append(file)
                continue
            date_folder = gate.joinpath(str(date))
            date_folder.mkdir(exist_ok=True)
            file = file.rename(date_folder.joinpath(file.name))
            date_files[date].append(file)
        date_files_all[gate.name] = date_files
    return date_files_all


def file_pair(file: Path) -> Tuple[Optional[Path], Optional[Path]]:
    if 'request' in file.stem:
        return None, None
    request_file = Path(str(file).replace('response', 'request'))
    if not request_file.exists():
        return None, file
    else:
        return request_file, file


def get_conversation(file: Path) -> Optional[FeigResponse]:
    """
    Read and parse a request and a response
    :param file: Response file
    :return: Response object
    """
    request_file, response_file = file_pair(file)
    if not response_file:
        return None
    if request_file:
        request_obj = FeigRequest.parse_request(request_file.read_bytes())
        response_obj = request_obj.parse_response(response_file.read_bytes())
    else:
        response_obj = FeigResponse.parse_response(response_file.read_bytes())

    return response_obj

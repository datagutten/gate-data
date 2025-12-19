import json
from pathlib import Path


def day_stats(file: Path):
    lowest_in = None
    highest_in = None
    lowest_out = None
    highest_out = None
    with file.open() as fp:
        data = json.load(fp)
    for timestamp, counts in data.items():
        if lowest_in is None or counts['in'] < lowest_in:
            lowest_in = counts['in']
        if lowest_out is None or counts['out'] < lowest_out:
            lowest_out = counts['out']

        if highest_in is None or counts['in'] > highest_in:
            highest_in = counts['in']
        if highest_out is None or counts['out'] > highest_out:
            highest_out = counts['out']
    return highest_in - lowest_in, highest_out - lowest_out, lowest_in, highest_in  # , lowest_out, highest_out

import json
import re
import sys
from pathlib import Path

from feig.people_count import day_stats

if __name__ == '__main__':
    stats = []
    for gate in Path(sys.argv[1]).iterdir():
        if not gate.is_dir():
            continue

        for date in gate.iterdir():
            if not date.is_dir() or not re.match(r'(\d{4}-\d{2}-\d{2})', date.name):
                continue

            people_in, people_out, day_min_in, day_max_in = day_stats(date.joinpath('PeopleCounterResponse.json'))
            stats.append({
                'gate': gate.name,
                'date': date.name,
                'people_in': people_in,
                'people_out': people_out,
            })
    with Path('people_count.json').open('w') as fp:
        json.dump(stats, fp)

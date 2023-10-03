import time
import json
import datetime
from pathlib import Path

import fire
import matplotlib.dates
import matplotlib.pyplot as plt


def ember(n):
    d = {}

    终 = int(time.time())//3600
    for i in range(终, 终-n, -1):
        p = Path.home() / f'.negate-hypnotic/{i}.json'
        if not p.exists():
            print(f'{p}不存在，跳过。')
            continue
        with open(p) as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    t, f, args = json.loads(line)
                except json.JSONDecodeError:
                    continue
                m = int(t) // 60
                d.setdefault(f, {}).setdefault(m, 0)
                d[f][m] += 1

    t = time.time()
    fig = plt.figure()

    for k, (f, dd) in enumerate(d.items()):
        for i in range(min(dd.keys()), max(dd.keys())):
            dd.setdefault(i, 0)
        x, y = zip(*sorted(dd.items()))
        x = [datetime.datetime.fromtimestamp(i*60) for i in x]
        sub = fig.add_subplot((len(d)-1)//2+1, 2, k+1)
        sub.set_title(f)
        sub.plot(x, y)

    plt.gca().xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%H:%M'))
    plt.tight_layout()
    plt.show()


fire.Fire(ember)

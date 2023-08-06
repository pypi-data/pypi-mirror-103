#!/usr/bin/env python3

import json
import pandas

data = []
with open('monit.json') as f:
    for line in f:
        data.append(json.loads(line))
df = pandas.DataFrame(data)
print(df)

from redgifs import API
from redgifs.utils import _read_tags_json
import os

api = API().login()
nt = api.get_tags()
ct = _read_tags_json()
wh = os.environ.get('DISCORD_WEBHOOK', None)

mapping = {
    tag.lower(): tag # type: ignore
    for tag in [d['name'] for d in nt]
}

with open('redgifs/tags.json', 'w') as f:
    import json
    json.dump(mapping, f)

before = len(ct)
with open('redgifs/tags.json') as f:
    now = len(json.load(f))
    print('Before:', before)
    print('Now:', now)
    print(f'Added {now - before} new tags')

if wh is not None:
    import requests
    tags = _read_tags_json()
    newtags = list(filter(lambda t: t not in ct.keys(), tags))
    r = requests.post(wh, json={
        'content': f'Added `{len(newtags)}` new tags.\n{", ".join(newtags)}'
    })
else:
    print('No Discord webhook found')

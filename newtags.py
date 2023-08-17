from redgifs import API
from redgifs.utils import _read_tags_json
api = API()
api.login()
nt = api.get_tags()
ct = _read_tags_json()

mapping = {
    tag.lower(): tag # type: ignore - checked below
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

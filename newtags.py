from redgifs import API
from redgifs.utils import _read_tags_json
import os

api = API().login()
new_tags = api.get_tags()
old_tags = _read_tags_json()
webhook = os.getenv('DISCORD_WEBHOOK', None)

new_tags = {
    tag.lower(): tag
    for tag in [d['name'] for d in new_tags]
}

before = len(old_tags)
now = len(new_tags)
print(f'There are {now - before} new tags')

if webhook is not None:
    with open('redgifs/tags.json', 'w') as f:
        import json
        json.dump(new_tags, f)

    import requests
    new = list(filter(lambda tag: tag not in old_tags.keys(), new_tags))
    r = requests.post(webhook, json={
        'content': f'Added `{len(new)}` new tags.\n{", ".join(new)}'
    })
else:
    new = list(filter(lambda tag: tag not in old_tags.keys(), new_tags))
    print('No Discord webhook found')
    print('The new tags added are:\n ', "\n  ".join(new))

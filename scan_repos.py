#!/usr/bin/env python3

import json
import os
import pandas as pd
import re
import tinydb
from decouple import config
from icecream import ic
from pathlib import Path
from sh import gh

# verbose icecream
ic.configureOutput(includeContext=True)

'''
Scan Repos

Call gh CLI to get a user's repo URLs,
then feed to TinyDB JSON,
scan w/___ red team tool (e.g., trufflehog)
'''

home = Path.home()
env = Path('.env')
cwd = Path.cwd()

if env.exists():
    username = config('USERNAME', default='', cast=str)
    limit = config('LIMIT', default=5, cast=int)
    visibility = config('VISIBILITY', default='public', cast=str)
else:
    username = os.getenv('USERNAME')
    limit = os.getenv('LIMIT')
    visibility = os.getenv('VISIBILITY')    # public, private, internal

raw = gh("repo", "list", username, "--limit", limit, "--visibility", visibility, "--json", "url")

# convert to utf-8
pub_repos = raw.stdout.decode('utf-8')

# strip ansi escape codes
# * https://stackoverflow.com/a/14693789
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
pub_repos = ansi_escape.sub('', pub_repos)

# df extract repo url
df = pd.read_json(pub_repos)
df = df[df['url'].str.startswith('https://')]

# create directory if it doesn't exist
db_dir = cwd/'raw'
Path.mkdir(db_dir, exist_ok=True)

# store the repo names as a tinydb database
db = tinydb.TinyDB(Path(f"{db_dir}/repos.json"))
db.insert(json.loads(df.to_json()))
ic(db.all())

# TODO: scan repo URLs

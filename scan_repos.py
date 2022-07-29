#!/usr/bin/env python3

import json
import pandas as pd
import re
import tinydb
from icecream import ic
from pathlib import Path
from sh import gh

'''
Scan Repos

Call gh CLI to get a user's repo URLs,
then feed to TinyDB JSON,
scan w/___ red team tool (e.g., trufflehog)
'''

home = Path.home()
username = 'pythoninthegrass'
lim = 5
vis = 'public'                  # public, private, internal

raw = gh("repo", "list", username, "--limit", lim, "--visibility", vis, "--json", "url")

# convert to utf-8
pub_repos = raw.stdout.decode('utf-8')

# strip ansi escape codes
# * https://stackoverflow.com/a/14693789
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
pub_repos = ansi_escape.sub('', pub_repos)

# df extract repo url
df = pd.read_json(pub_repos)
df = df[df['url'].str.startswith('https://')]

# store the repo names as a tinydb database
db = tinydb.TinyDB(Path(f"{home}/Downloads/repos.json"))
db.insert(json.loads(df.to_json()))
# ic(db.all())

# TODO: scan repo URLs

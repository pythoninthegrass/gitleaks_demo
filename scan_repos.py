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

home = Path.home()
env = Path('.env')
cwd = Path.cwd()
db_dir = cwd/'raw'
fn = Path(f"{cwd}/raw/repos.json")

# create directory if it doesn't exist
Path.mkdir(db_dir, exist_ok=True)

# env vars
if env.exists():
    username = config('USERNAME', default='', cast=str)
    limit = config('LIMIT', default=5, cast=int)
    visibility = config('VISIBILITY', default='public', cast=str)
else:
    username = os.getenv('USERNAME')
    limit = os.getenv('LIMIT')
    visibility = os.getenv('VISIBILITY')    # public, private, internal


def get_repos(username, limit, visibility):
    '''Get the repos for a user'''
    if not fn.exists():
        raw = gh("repo", "list", username, "--limit", limit, "--visibility", visibility, "--json", "url")

        # convert to utf-8
        pub_repos = raw.stdout.decode('utf-8')

        # strip ansi escape codes
        # * https://stackoverflow.com/a/14693789
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        pub_repos = ansi_escape.sub('', pub_repos)

        # extract repo url
        df = pd.read_json(pub_repos)
        df = df[df['url'].str.startswith('https://')]
    else:
        df = pd.read_json(fn)

    return df


def write_repos(fn, df=None):
    '''Store the repo names as a tinydb database'''
    if not fn.exists():
        db = tinydb.TinyDB(Path(fn))
        db.insert(json.loads(df.to_json()))
    else:
        db = tinydb.TinyDB(Path(fn))

    return db


def read_repos(db):
    '''Read the repo names from the tinydb database'''
    return ic(db.all())


def main():
    df = get_repos(username, limit, visibility)
    db = write_repos(fn, df)

    return read_repos(db)


# TODO: scan repo URLs
if __name__ == "__main__":
    main()

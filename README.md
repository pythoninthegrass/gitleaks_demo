# gitleaks_demo

![hackermancat](img/octocat_hackerman.png)

## Summary
Learning a programming language is hard. Not committing secrets [doesn't have to be that way](https://github.com/zricethezav/gitleak).


**Table of Contents**
* [gitleaks_demo](#gitleaks_demo)
  * [Summary](#summary)
  * [Setup](#setup)
  * [Usage](#usage)
  * [TODO](#todo)
  * [Red Team Exercise](#red-team-exercise)
  * [Further Reading](#further-reading)

## Setup
* `gitleaks` install
```bash
# source
git clone https://github.com/zricethezav/gitleaks.git
cd gitleaks
make build

# brew
brew install gitleaks
```
* pre-commit
```bash
# pip
pip install pre-commit

# brew
brew install pre-commit

# install .pre-commit-config.yaml
pre-commit install

# test
λ pre-commit install
pre-commit installed at .git/hooks/pre-commit
λ pre-commit run --all-files
[INFO] Initializing environment for https://github.com/zricethezav/gitleaks.
[INFO] Installing environment for https://github.com/zricethezav/gitleaks.
[INFO] Once installed this environment will be reused.
[INFO] This may take a few minutes...
Detect hardcoded secrets.................................................Passed
```
* `bfg` install
```bash
# env
username=rtyley
projectname=bfg-repo-cleaner

# extract bfg version number then download bin from alternate host
ver=$(curl -s https://api.github.com/repos/${username}/${projectname}/releases/latest | grep tag_name | cut -d '"' -f 4 | sed 's/[^0-9\.]//g')
url="https://repo1.maven.org/maven2/com/madgag/bfg/${ver}/bfg-${ver}.jar"
curl -LJO $url && mv bfg-${ver}.jar bfg.jar
mv bfg.jar /usr/local/bin/bfg
```

## Usage
* `git commit`
```bash
# commit a secret
SKIP=gitleaks git commit -m "skip gitleaks check"

# don't commit a secret
git commit -m "this commit contains a secret"
```
* `gitleaks detect`
```bash
# local scan
export GITLEAKS_CONFIG=$(pwd)/gitleaks.toml
export GITLEAKS_REPORT=$(pwd)/gitleaks_report.json
gitleaks detect
gitleaks detect -r $GITLEAKS_REPORT
gitleaks detect --no-git
gitleaks detect --no-git -r $GITLEAKS_REPORT
```
* `bfg`
```bash
# remove the offending file first
git rm .env

# clone problem child
git clone --mirror git@github.com:pythoninthegrass/gitleaks_demo.git

# delete file
λ java -jar $(which bfg) --delete-files .env gitleaks_demo.git

Using repo : gitleaks_demo.git

Found 23 objects to protect
Found 2 commit-pointing refs : HEAD, refs/heads/main

Protected commits
-----------------

These are your protected commits, and so their contents will NOT be altered:

 * commit bd45c07e (protected by 'HEAD')
<SNIP>
Deleted files
-------------

        Filename   Git id           
        ----------------------------
        .env     | c48f0d38 (646 B )

# strip references in commit history
cd gitleaks_demo.git
git reflog expire --expire=now --all && git gc --prune=now --aggressive

# push changes
git push        # `-f` to force -- destructive
```

## TODO
* `settings.json` leak not detected
* ~~Attempt to commit `.env` after commenting out in `.gitignore`~~

## Red Team Exercise
Look for any leaked cloud keys

Attempt to abuse the access you get (e.g., can you find any admin passwords?)

## Further Reading
[zricethezav/gitleaks: Protect and discover secrets using Gitleaks 🔑](https://github.com/zricethezav/gitleaks)

[pre-commit](https://pre-commit.com/)

[bfg download](https://github.com/Installomator/Installomator/blob/main/Installomator.sh#L490)

[bfg usage](https://rtyley.github.io/bfg-repo-cleaner/)

[bfg regex](https://gist.github.com/w0rd-driven/60779ad557d9fd86331734f01c0f69f0?permalink_comment_id=3985799#gistcomment-3985799)

[Top 9 Git Secret Scanning Tools for DevSecOps - Spectral](https://spectralops.io/blog/top-9-git-secret-scanning-tools/)

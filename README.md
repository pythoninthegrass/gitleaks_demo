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
* gitleaks
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

## TODO
* `settings.json` leak not detected
* ~~Attempt to commit `.env` after commenting out in `.gitignore`~~

## Red Team Exercise
Look for any leaked cloud keys

Attempt to abuse the access you get (e.g., can you find any admin passwords?)

## Further Reading
[zricethezav/gitleaks: Protect and discover secrets using Gitleaks 🔑](https://github.com/zricethezav/gitleaks)

[pre-commit](https://pre-commit.com/)

[Top 9 Git Secret Scanning Tools for DevSecOps - Spectral](https://spectralops.io/blog/top-9-git-secret-scanning-tools/)

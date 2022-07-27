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
  * [Further Reading](#further-reading)

## Setup
`TODO`

## Usage
```bash
# TODO: documentme
export GITLEAKS_CONFIG=$(pwd)/gitleaks.toml
export GITLEAKS_REPORT=$(pwd)/gitleaks_report.json
gitleaks detect
gitleaks detect -r $GITLEAKS_REPORT
gitleaks detect --no-git
gitleaks detect --no-git -r $GITLEAKS_REPORT
```

## TODO
* `settings.json` leak not detected
* Attempt to commit `.env` after commenting out in `.gitignore`

## Red Team Exercise

Look for any leaked cloud keys

Attempt to abuse the access you get (e.g can you find any admin passwords?)

## Further Reading
[zricethezav/gitleaks: Protect and discover secrets using Gitleaks 🔑](https://github.com/zricethezav/gitleaks)

[Top 9 Git Secret Scanning Tools for DevSecOps - Spectral](https://spectralops.io/blog/top-9-git-secret-scanning-tools/)

# gitleaks_demo

![hackermancat](img/octocat_hackerman.png)

## Summary
Learning a programming language is hard. Not committing secrets [doesn't have to be that way](https://github.com/zricethezav/gitleak).

This repo covers the content from the Meetup [presentation](https://docs.google.com/presentation/d/e/2PACX-1vRDZHJBZPgJpfMF-eR7-cBHJHuM6seu2Nr78pbCFf-DHsGtgx6U_f_PFzQ9LpUIZGl71cgaDR1kZI30/pub?start=false&loop=false&delayms=3000&slide=id.p), [Securing GitHub Repos](https://www.meetup.com/okccoffeeandcode/events/287355886/) given on July 30th, 2022 at [Tailwind](https://www.tailwindapp.com/) by [sw33tr0ll](https://github.com/sw33tr0ll) and [pythoninthegrass](https://github.com/pythoninthegrass).

Testing has primarily been done on macOS, but it's likely most of the code works on Linux. Windows has not been tested. PRs welcome 🙏 

**Table of Contents**
* [gitleaks\_demo](#gitleaks_demo)
  * [Summary](#summary)
  * [Running the Target App](#running-the-target-app)
  * [Gitleaks Setup](#gitleaks-setup)
  * [Gitleaks Usage](#gitleaks-usage)
    * [Blue Team](#blue-team)
    * [Red Team](#red-team)
  * [TODO](#todo)
  * [Further Reading](#further-reading)

## Running the Target App
* Install [docker-compose](https://docs.docker.com/compose/install/)
* Set either `.env` or env vars for `ACCESS_KEY_ID` and `SECRET_ACCESS_KEY` (see: `.env.example`)
  * Need to uncomment `docker-compose.yml` code blocks for mutually exclusive choices (`env_file` vs. `environment`)
* Setup the Docker container
    ```bash
    # multistage build
    docker-compose build --parallel --force-rm

    # start container
    docker-compose up
    ```
* Navigate to http://localhost:8000/ in a web browser


## Gitleaks Setup
* `gitleaks` install
    ```bash
    # source
    git clone https://github.com/zricethezav/gitleaks.git
    cd gitleaks
    make build
    sudo chown root:root /usr/local/bin/gitleaks
    sudo mv gitleaks /usr/local/bin/

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
    pre-commit install                  # install/uninstall

    # test
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
    curl -LJO $url && mv bfg-${ver}.jar /usr/local/bin/bfg
    ```
* Install [asdf](https://asdf-vm.com/guide/getting-started.html#_2-download-asdf)
* Install Python 3.10.5
    ```bash
    # add python plugin
    asdf plugin-add python

    # install stable python
    asdf install python 3.10.5

    # refresh symlinks for installed python runtimes
    asdf reshim python
    ```
* Install [poetry](https://python-poetry.org/docs/)
* Install Python environment
    ```bash
    # pip
    # python3.10 -m pip install -r requirements.txt

    # poetry (preferred)
    poetry install
    ```
* `trufflehog` install
    ```bash
    brew tap trufflesecurity/trufflehog
    brew install trufflehog
    ```

## Gitleaks Usage
### Blue Team
* `git commit`
    ```bash
    # commit a secret
    SKIP=gitleaks git commit -m "skip gitleaks check"

    # don't commit a secret
    git commit -m "this commit contains a secret"
    ```
* `gitleaks detect`
  * Local Scan
    ```bash
    # export environment variables
    export GITLEAKS_CONFIG=$(pwd)/gitleaks.toml
    export GITLEAKS_REPORT=$(pwd)/gitleaks_report.json

    # run verbose scan with creds redacted...
    gitleaks detect --redact -v

    # ... and generate report
    gitleaks detect --redact -v -r $GITLEAKS_REPORT

    # scan local directories ignoring git logs
    gitleaks detect --redact -v --no-git
    gitleaks detect --redact -v --no-git -r $GITLEAKS_REPORT
    ```
* `bfg`
    ```bash
    # remove the offending file from git history (leaves local copy)
    git rm --cached .env

    # clone problem child
    cd ~/Downloads
    git clone --mirror git@github.com:pythoninthegrass/gitleaks_demo.git

    # delete file
    λ java -jar /usr/local/bin/bfg --delete-files .env ~/Downloads/gitleaks_demo.git

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
    cd ~/Downloads/gitleaks_demo.git
    git reflog expire --expire=now --all && git gc --prune=now --aggressive

    # force push changes (rewrite repo history to remove sensitive data)
    git push -f

    # OPTIONAL: if the remote rejects `git push -f` (e.g., PR removed branch)
    # remove references within mirrored repo
    #  - [deleted]         dev
    #  + 681f990...0e35aa3 main -> main (forced update)
    #  ! [remote rejected] refs/pull/5/head -> refs/pull/5/head (deny updating a hidden ref)
    # error: failed to push some refs to 'github.com:pythoninthegrass/gitleaks_demo.git
    # git show-ref | cut -d' ' -f2 | grep 'pull' | xargs -r -L1 git update-ref -d

    # update full repo (needs rebase to avoid fast-forward error)
    cd ~/git/gitleaks_demo
    λ git pull --rebase
    Successfully rebased and updated refs/heads/main.
    λ git push
    Enumerating objects: 5, done.
    <SNIP>
    remote: Resolving deltas: 100% (2/2), completed with 2 local objects.
    To github.com:pythoninthegrass/gitleaks_demo.git
    dc1323a..be09c98  main -> main

    # remove any lingering creds in-place
    cd ~/Downloads
    rm -rf ~/Downloads/gitleaks_demo.git
    git clone --mirror git@github.com:pythoninthegrass/gitleaks_demo.git
    # REDACT secret in file or append `--no-blob-protection` to bfg command below (destructive)
    java -jar /usr/local/bin/bfg -fe rem.txt --replace-text rem.txt gitleaks_demo.git       # filter-excluding '*.{xml,pdf}'
    cd ~/Downloads/gitleaks_demo.git
    git reflog expire --expire=now --all && git gc --prune=now --aggressive
    git push -f
    cd ~/git/gitleaks_demo
    git add README.md
    git commit -m "Update README.md"                                                        # commit any pending changes
    git pull --rebase
    git push
    ```
* `trufflehog`
  * Set either `.env` or env vars for `USERNAME`, `LIMIT`, and `VISIBILITY` (see: `.env.example`)
    ```bash
    # run script
    # python3.10 scan_repos.py          # pip
    poetry run python scan_repos.py     # poetry
    ```

### Red Team
* Look for any leaked cloud keys
* Attempt to abuse the access you get (e.g., can you find any admin passwords?)

## TODO
* `settings.json` leak not detected (custom gitleaks regex needed)

## Further Reading
[zricethezav/gitleaks: Protect and discover secrets using Gitleaks 🔑](https://github.com/zricethezav/gitleaks)

[pre-commit](https://pre-commit.com/)

[Is it better to use git pull --rebase than git pull --ff-only - Stack Overflow](https://stackoverflow.com/questions/64846230/is-it-better-to-use-git-pull-rebase-than-git-pull-ff-only)

[Removing sensitive data from a repository - GitHub Docs](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)

[Encrypted secrets - GitHub Docs](https://docs.github.com/en/actions/security-guides/encrypted-secrets)

[Securing your repository - GitHub Docs](https://docs.github.com/en/code-security/getting-started/securing-your-repository)

[Environment variables in Compose | Docker Documentation](https://docs.docker.com/compose/environment-variables/)

[linux - How do I delete an exported environment variable? - Stack Overflow](https://stackoverflow.com/questions/6877727/how-do-i-delete-an-exported-environment-variable/6877747#6877747)

[bfg download](https://github.com/Installomator/Installomator/blob/main/Installomator.sh#L490)

[bfg usage](https://rtyley.github.io/bfg-repo-cleaner/)

[bfg regex](https://gist.github.com/w0rd-driven/60779ad557d9fd86331734f01c0f69f0?permalink_comment_id=3985799#gistcomment-3985799)

[bash - git push --mirror without pull refs - Stack Overflow](https://stackoverflow.com/questions/47776357/git-push-mirror-without-pull-refs)

[Top 9 Git Secret Scanning Tools for DevSecOps - Spectral](https://spectralops.io/blog/top-9-git-secret-scanning-tools/)

[![GitHub license](https://img.shields.io/github/license/Rollcloud/whathappened)](https://github.com/Rollcloud/whathappened/blob/main/LICENSE)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/Rollcloud/whathappened/test-build?logo=github)](https://github.com/Rollcloud/whathappened/actions?query=workflow%3Atest-build)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/whathappened?logo=pypi)](https://pypi.org/project/whathappened/)
[![semver](https://img.shields.io/badge/semver-2.0.0-blue)](https://semver.org/)
[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/rollcloud/whathappened?sort=semver)](https://github.com/Rollcloud/whathappened/releases)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# whathappened
A changelog generator using simply structured git commit messages

## Inspired by

* [SemVer](https://semver.org/)
* [Angular Commit Message Format](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit)
* [Auto Changelog](https://github.com/Michael-F-Bryan/auto-changelog)
* [git_commits.py](https://gist.github.com/simonw/091b765a071d1558464371042db3b959#file-get_commits-py)

## Install and Run

Installation is as simple as it gets:

    $ pip install whathappened

To generate a changelog, run:

    $ whathappened

Make sure to activate any virtual environment that you might be using first.

Some options are available:

    $ whathappened --help
    Usage: whathappened [OPTIONS] [GIT_LOG_ARGS]...

      Handle command line arguments. Extra arguments are passed to 'git log'.

    Options:
      --overriding-version TEXT  Specify a version number to use [format: x.y.z]
      -o, --output PATH  The changelog destination [default: stdout]
      -e, --emoji        Include emoji in headings if present
      -p, --prefix TEXT  Version prefix, often 'version' or 'v' [default: '']
      
      --version          Show the version and exit.
      --help             Show this message and exit.

To limit the range of commits, add a [`revision range`](https://git-scm.com/docs/git-log#Documentation/git-log.txt-ltrevisionrangegt) argument.

To create a changelog of commits that are yet to be pushed:

    $ whathappened origin..HEAD

To create a changelog of commits between (branch: main) and (tag: v1.0.0) and write the output to file:

    $ whathappened -o CHANGELOG.md main..v1.0.0

## Package Changelog

Created by Whathappened itself - very meta.

For the complete changelog, please see [CHANGELOG.md](CHANGELOG.md).

## Whathappened Commit Message Format

For a full description of the message format, see [Commit-It-Simple](https://commit-it-simple.github.io/).

Whathappened expects git commit messages in the format outlined below:

    [optional breaking ]<type>[ optional (<scope>)]: <description>

    [optional body]

`<type>` is recommended to be one of:

    fix
    feat
    build
    ci
    docs
    style
    refactor
    perf
    test

Variations on these types like `feat, feature, features`, or `doc, docs` are seamlessly grouped together.

The `<scope>` is recommended to be a module, file, or folder name as appropriate.

More examples can be viewed on whathappened's own [commits](https://github.com/Rollcloud/whathappened/commits/).

For a nice summary of `type`s and what they mean, please see [Understanding Semantic Commit Messages Using Git and Angular](https://nitayneeman.com/posts/understanding-semantic-commit-messages-using-git-and-angular/).

## Emoji

Adding the `--emoji` flag will add emoji after each heading in the changelog. Below is the list of emoji that are used:

* Docs 📝
* Features ✨
* Fixes 🐛
* Performance ⚡️
* Refactorings ♻️
* Other 🃏 

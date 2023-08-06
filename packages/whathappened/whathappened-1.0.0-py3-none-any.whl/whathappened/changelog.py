import re

from datetime import datetime
from itertools import groupby

# imported to make this module the base module for all external calls to functions
try:
    from whathappened.git_commits import get_commits  # noqa
except ImportError:  # for development use
    from git_commits import get_commits  # noqa

# https://semver.org/spec/v2.0.0.html
semver_regex = re.compile(
    r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)"
    r"(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
    r"(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)


class VersionFormatException(Exception):
    """Raise when a version string cannot be correctly parsed."""

    pass


class Version:
    """
    All the changes committed prior to a new version being released.

    Also includes their attributes, such as breaking, feature, or fix.
    """

    def __init__(self, ref, date):
        self.ref = ref
        self.date = (
            datetime.strptime(date, "%a %b %d %H:%M:%S %Y %z")
            if isinstance(date, str)
            else date
        )  # str input format Wed Apr 22 18:58:54 2020 +0200

        self.breaking = 0
        self.feature = 0
        self.fix = 0

        self.commits = []

    def __repr__(self):
        return (
            f"Version('{self.ref}',"
            f" {self.date},"
            f" breaking={self.breaking},"
            f" feature={self.feature},"
            f" fix={self.fix},"
            f" num_commits={len(self.commits)})"
        )  # pragma: no cover


class Commit:
    """The content and attributes of a single Git commit."""

    commit_regex = re.compile(
        r"(?:(?P<breaking>break(?:ing)?)? ?(?P<type>\w+){1}"
        r" ?(?:\((?P<scope>[^\(\):]+)\))?: (?P<description>.+)|"
        r"(?P<description_alt>.+))",
        flags=re.IGNORECASE,
    )

    def __init__(self, commit_dict):
        self.commit_dict = commit_dict

    def __getattr__(self, name):

        try:
            return self.commit_dict[name]
        except KeyError:

            result = Commit.commit_regex.match(self.title)
            breaking, commit_type, scope, description, description_alt = (
                result.group('breaking'),
                result.group('type'),
                result.group('scope'),
                result.group('description'),
                result.group('description_alt'),
            )

            if name == 'description':
                return description if description is not None else description_alt
            elif name == 'is_breaking':
                return breaking is not None
            elif name == 'type':
                # group equivalent commit types
                types = {
                    'doc': 'docs',
                    'docs': 'docs',
                    'feat': 'feat',
                    'feature': 'feat',
                    'features': 'feat',
                    'fix': 'fix',
                    'fixes': 'fix',
                    'perf': 'perf',
                    'performance': 'perf',
                    'refac': 'refactor',
                    'refactor': 'refactor',
                }
                try:
                    return types[commit_type]
                except KeyError:
                    return commit_type if commit_type is not None else 'other'
            elif name == 'scope':
                return scope
            elif name == 'is_feature':
                return "feat" in self.type.lower()
            elif name == 'is_fix':
                return "fix" in self.type.lower()
            else:
                raise AttributeError(f"Attribute '{name}' not found in class Commit")

    def __repr__(self):
        return (
            f"Commit({{"
            f"'hash': '{self.hash[:6]}', "
            f"'title': '{self.title}', "
            f"}})"
        )  # pragma: no cover


def _sentence(string):
    """Format a given string in sentence case."""
    try:
        return string[0].upper() + string[1:]
    except IndexError:
        # zero-length string
        return string


def calculate_next(versions, prefix=""):
    """
    Calculate the next version number to be released.

    Based on changes made since the previous version.
    """
    global semver_regex

    try:
        previous = versions[1]
    except IndexError:
        # if no previous version has been found
        return f"{prefix}0.1.0"

    previous_version = previous.ref[len(prefix) :]
    result = semver_regex.match(previous_version)

    # extract version numbers if possible:
    try:
        major, minor, patch = (
            int(result.group('major')),
            int(result.group('minor')),
            int(result.group('patch')),
        )
    except AttributeError:
        raise VersionFormatException(
            f"The version number of '{previous_version}' with prefix='{prefix}' cannot"
            f" be parsed. Please enter the appropriate prefix or use a version string"
            f" like 'X.Y.Z'. See https://semver.org/spec/v2.0.0.html for more details."
        )

    latest_version = versions[0]

    if major == 0:
        # this is a development release and only receives minor and patch increments
        if latest_version.breaking > 0:
            return f"{prefix}{major}.{minor+1}.0"
        elif latest_version.feature > 0 or latest_version.fix > 0:
            return f"{prefix}{major}.{minor}.{patch+1}"
        else:
            # no api changes
            return f"{prefix}{major}.{minor}.{patch}"

    else:
        # this is production release and receives major, minor, and patch increments
        if latest_version.breaking > 0:
            return f"{prefix}{major+1}.0.0"
        elif latest_version.feature > 0:
            return f"{prefix}{major}.{minor+1}.0"
        elif latest_version.fix > 0:
            return f"{prefix}{major}.{minor}.{patch+1}"
        else:
            # no api changes
            return f"{prefix}{major}.{minor}.{patch}"


def compile_log(commits):
    """Iterate though a list of Commits, compiling a list of Versions based on tags."""
    versions = []

    # iterate through commits from latest to earliest

    # group by version
    for commit in commits:
        # make a new version if required
        if len(commit['tags']) > 0 or len(versions) == 0:
            tag = commit['tags'][0] if len(commit['tags']) > 0 else 'HEAD'
            versions.append(Version(ref=tag, date=commit['date']))

        this_commit = Commit(commit)

        # append to current version
        versions[-1].commits.append(this_commit)

        # check if commit is breaking, feature, or fix
        if this_commit.is_breaking:
            versions[-1].breaking += 1

        if this_commit.is_feature:
            versions[-1].feature += 1

        if this_commit.is_fix:
            versions[-1].fix += 1

    # for version in versions:
    #     print(version)

    return versions


def update_latest_version(versions, prefix=""):
    """Update the HEAD reference to show the next semver version."""
    latest_version = versions[0]
    latest_version.ref = calculate_next(versions, prefix=prefix)

    return versions


def override_latest_version(versions, overriding, prefix=""):
    """Update the HEAD reference to show the overriding version."""
    latest_version = versions[0]
    latest_version.ref = f"{prefix}{overriding}"

    return versions


def format_log(versions, emoji=False):
    """Produce a nicely formatted changelog - with emoji too if required."""
    output = "# Changelog"

    headings = {
        'docs': "Docs 📝",
        'feat': "Features ✨",
        'fix': "Fixes 🐛",
        'perf': "Performance ⚡️",
        'refactor': "Refactorings ♻️",
        'other': "Other 🃏",
    }

    if not emoji:
        # remove emoji (first two characters) from headings, and strip space character
        headings = {key: heading[:-2].strip() for key, heading in headings.items()}
    else:
        # leave emoji in headings
        pass

    for version in versions:
        output += f"\n\n## {version.ref} ({version.date.isoformat()[:10]})\n"

        # store groupby results as lists
        groups = []
        uniquekeys = []
        data = sorted(version.commits, key=lambda x: x.type[:4])
        for k, g in groupby(data, lambda x: x.type):
            groups.append(list(g))  # Store group iterator as a list
            uniquekeys.append(k)

        headings_in_this_version = [k for k in uniquekeys if k in headings]

        for key, group in zip(uniquekeys, groups):
            if key in headings:

                # check if Other is the only heading in this version
                if key == 'other' and len(headings_in_this_version) == 1:
                    # if it is, it is redundent and should not be displayed
                    output += "\n"
                else:
                    # else display the heading as usual
                    output += f"\n### {headings[key]}\n\n"

                for commit in sorted(group, key=lambda x: f"{x.scope} {x.description}"):
                    scope = f"{commit.scope} - " if commit.scope else ''
                    desc = commit.description.replace('_', '\\_')  # escape underscore
                    desc = _sentence(desc) if len(scope) == 0 else desc
                    breaking = " [BREAKING]" if commit.is_breaking else ''
                    output += f"* {_sentence(scope)}{desc}{breaking}\n"

    return output


def write_log(log, filename):
    with open(filename, 'w') as f:
        f.write(log)

import click

try:
    from whathappened import __version__, changelog
except ImportError:  # for development use
    import changelog

    __version__ = 'major.minor.patch'


def main(
    output="CHANGELOG.md",
    overriding_version=None,
    emoji=False,
    prefix="",
    git_log_args=[],
):
    commits = changelog.get_commits(git_log_args=git_log_args)
    versions = changelog.compile_log(commits)
    versions = (
        changelog.update_latest_version(versions, prefix=prefix)
        if overriding_version is None
        else changelog.override_latest_version(
            versions, overriding_version, prefix=prefix
        )
    )
    log = changelog.format_log(versions, emoji=emoji)

    if output is not None:
        changelog.write_log(log, output)
    else:
        click.echo(log)


@click.command(context_settings=dict(ignore_unknown_options=True))
@click.option(
    '--overriding-version',
    default=None,
    help="Specify a version number to use [format: x.y.z]",
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    default=None,
    help="The changelog destination [default: stdout]",
)
@click.option(
    '--emoji',
    '-e',
    is_flag=True,
    default=False,
    help="Include emoji in headings if present",
)
@click.option(
    '--prefix',
    '-p',
    default="",
    help="Version prefix, often 'version' or 'v' [default: '']",
)
@click.argument('git_log_args', nargs=-1, type=click.UNPROCESSED)
@click.version_option(version=__version__)
def cli(output, overriding_version, emoji, prefix, git_log_args):
    """
    Handle command line arguments. Extra arguments are passed to 'git log'.
    """
    main(
        output=output,
        overriding_version=overriding_version,
        emoji=emoji,
        prefix=prefix,
        git_log_args=git_log_args,
    )


if __name__ == '__main__':
    cli()

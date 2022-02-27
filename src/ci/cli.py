#!/usr/bin/env python3
from ci.run import group as runner

import click
import coloredlogs
import warnings

warnings.filterwarnings("ignore")

command_groups = [runner]


@click.group()
def entry_point():
    pass


def main():

    coloredlogs.install(fmt="%(asctime)s %(name)s %(levelname)s %(message)s")

    for group in command_groups:
        entry_point.add_command(group)

    # Special command without group
    entry_point()


if __name__ == "__main__":
    main()

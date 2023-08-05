"""Entry point for the CLI (Init of parser)"""

#!/usr/bin/python3
import argparse

from .apps import AppsCommmand
from .auth import AuthCommand
from .deploy import DeployCommand
from .scaffold import CreateCommand


def main():
    parser = argparse.ArgumentParser(
        description="deepchain cli", add_help=True, usage="deepchain <command> [<args>]"
    )
    commands_parser = parser.add_subparsers(help="deepchain-cli command helpers")

    AuthCommand.register_subcommand(commands_parser)
    CreateCommand.register_subcommand(commands_parser)
    DeployCommand.register_subcommand(commands_parser)
    AppsCommmand.register_subcommand(commands_parser)

    args = parser.parse_args()
    service = args.func(args)
    service.run()


if __name__ == "__main__":
    main()

"""Entry point for the CLI (Init of parser)"""

#!/usr/bin/python3 # noqa: E265
import argparse

from .apps import AppsCommmand
from .auth import AuthCommand
from .deploy import DeployCommand
from .scaffold import CreateCommand


def main():
    parser = argparse.ArgumentParser(
        description="deepchain CLI",
        add_help=True,
        usage="deepchain <command> [--<args>] [<arguments>]",
    )
    commands_parser = parser.add_subparsers(help="deepchain-cli command helpers")

    AuthCommand.register_subcommand(commands_parser)
    CreateCommand.register_subcommand(commands_parser)
    DeployCommand.register_subcommand(commands_parser)
    AppsCommmand.register_subcommand(commands_parser)

    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        exit(1)

    service = args.func(args)
    service.run()


if __name__ == "__main__":
    main()

"""Commands to provide additional feature on app, such as list all the apps"""
from argparse import ArgumentParser

from deepchain import log
from deepchain.cli import BaseCLICommand

from .apps_utils import (
    display_apps_infos,
    display_config_info,
    get_apps_config,
    remove_app,
    reset_apps,
)


def app_command_factory(args):
    return AppsCommmand(args.infos, args.reset, args.delete, args.config)


class AppsCommmand(BaseCLICommand):
    def __init__(self, infos: bool, reset: bool, delete: str, config: bool):
        self.infos = infos
        self.reset = reset
        self.delete = delete
        self.config = config

    @staticmethod
    def register_subcommand(parser: ArgumentParser):
        apps_parser = parser.add_parser(name="apps", help="give infos on apps create locally")

        apps_parser.add_argument(
            "--infos",
            action="store_true",
            help="list all apps' infos",
        )

        apps_parser.add_argument(
            "--reset",
            action="store_true",
            help="!reset all apps",
        )

        apps_parser.add_argument(
            "--delete",
            type=str,
            default=None,
            help="delete selected app",
        )

        apps_parser.add_argument(
            "--config",
            action="store_true",
            help="show URL deployement config",
        )

        apps_parser.set_defaults(func=app_command_factory)

    def run(self):
        if self.infos:
            config = get_apps_config()

            if len(config) == 0:
                print("-------------------")
                print("No apps to display")
                print("-------------------")
            else:
                display_apps_infos(config)

        if self.config:
            display_config_info()

        if self.reset:
            msg = "You are about to delete all your apps, do you want to continue? (y/n) "
            answer = input(msg)
            while answer not in ["y", "n"]:
                answer = input(msg)

            if answer == "y":
                reset_apps()

        if self.delete is not None:
            msg = f"You are about to delete {self.delete}' files, do you want to continue? (y/n) "
            answer = input(msg)
            while answer not in ["y", "n"]:
                answer = input(msg)

            if answer == "y":
                remove_app(self.delete)
                log.info("Remove App %s", self.delete)

"""Base functions to make the CLI working"""
import configparser
import importlib
import os
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Union

import pkg_resources
import yaml

from deepchain import AppNotFoundError, AppsNotFoundError, ConfigNotFoundError


def display_apps_infos(config: Dict) -> None:
    """Display apps infos

    Print a format table with three columns:
    ----------------------------------------
    APP             PATH              STATUS
    ----------------------------------------
    my_app         path/to/app      status

    Args:
        config (Dict): dictionary with directory and status for each app

    Returns:
        None
    """
    data_list = []
    data_list.append(["APP", "PATH", "STATUS"])
    for app, info in config.items():
        data_list.append([app, info["dir"], info["status"]])

    dash = "-" * 125

    for i, data in enumerate(data_list):
        if i == 0:
            print(dash)
            print("{:<20s}{:^90s}{:>15s}".format(data[0], data[1], data[2]))
            print(dash)
        else:
            print("{:<20s}{:^90s}{:>15s}".format(data[0], data[1], data[2]))

    return


def display_config_info() -> None:
    """
    Display the config where the URL is deployed
    """
    config = configparser.ConfigParser()
    path_config = pkg_resources.resource_filename("deepchain", "cli/config.ini")
    config.read(path_config)
    url = config["APP"]["DEEP_CHAIN_URL"]

    msg = f"App deployed at : {url}"
    dash = "-" * len(msg)
    print(dash)
    print(msg)
    print(dash)


def reset_apps() -> None:
    """
    Remove all apps' files
    """
    path = Path.home().joinpath(".deep-chain").joinpath("apps")
    apps_config = get_apps_config()

    if len(apps_config) > 0:
        for _, info in apps_config.items():
            try:
                shutil.rmtree(info["dir"])
            except FileNotFoundError:
                pass
        os.remove(str(path))
        path.touch(exist_ok=True)


def remove_app(app_name: str) -> None:
    """Remove the specified app name

    Args:
        app_name (str): app registered in .deepchain/apps

    Raises:
        AppNotFoundError: Error is app nos exists
    """

    data = get_apps_config()
    path = Path.home().joinpath(".deep-chain").joinpath("apps")

    app_info = data.get(app_name, None)
    if app_info is None:
        raise AppNotFoundError(app_name)

    try:
        shutil.rmtree(app_info["dir"])
    except FileNotFoundError:
        pass

    del data[app_name]
    with open(path, "w") as app_file:
        yaml.dump(data, app_file, Dumper=yaml.SafeDumper)


def get_app_info(app_name: str, kind: str = "dir") -> str:
    """
    Get information of an application.
    Args:
        app_name (str): [description]
        kind (str, optional):Defaults to "dir".
                        - dir : the directory of storage
                        - status : the status of the app (local or upload)

    Raises:
        AppNotFoundError: Error is app nos exists

    Returns:
        str: directory or status
    """
    assert kind in ["dir", "status"], "Can on only select 'dir' or 'status'"

    config = get_apps_config()
    app_info = config.get(app_name, None)

    if app_info is None:
        raise AppNotFoundError(app_name)

    return app_info[kind]


def get_apps_config() -> Dict:
    """Get app config file

    Raises:
        AppsNotFoundError: Error is .deepchain/apps file not exists

    Returns:
        Dict: dictionnary of {app: {dir:_,status:_}}
    """
    path = Path.home().joinpath(".deep-chain").joinpath("apps")
    if not path.is_file():
        raise AppsNotFoundError

    with open(path, "r") as apps_file:
        data = yaml.load(apps_file, Loader=yaml.SafeLoader)
        data = {} if data is None else data

    return data


def check_app_exist(app_name: str) -> Tuple[bool, Union[str, None]]:
    """
    Check if an app has always been created locally on the
    computer

    Args:
        app_name (str): name of the application

    Returns:
        Tuple[bool, str]: return is the app exist and Filename
    """
    config = get_apps_config()
    app_info = config.get(app_name, None)

    if app_info is not None:
        return True, app_info["dir"]
    else:
        return False, None


def save_app(app_name: str, dest_path: str) -> None:
    """
    Save complete path where the app is stored
    The app can be deploy next from any folder

    Args:
        app_name (str): application name stored in .deepchain/apps
        dest_path (str): folder for registraction of the app
    """
    root_path = _create_deechpain_folder()
    path = _create_apps_file(root_path)
    data = get_apps_config()

    data[app_name] = {"dir": os.path.abspath(dest_path), "status": "local"}
    with open(path, "w") as app_file:
        yaml.dump(data, app_file, Dumper=yaml.SafeDumper)


def update_app_status(app_name: str, status: str = "upload") -> None:
    """update the status of the app

    Args:
        app_name (str): name of application
        status (str, optional): status to update (local/upload). Defaults to "upload".
    """

    path = Path.home().joinpath(".deep-chain").joinpath("apps")
    data = get_apps_config()
    app_info = data.get(app_name, None)
    if app_info is None:
        raise AppNotFoundError(app_name)

    data[app_name]["status"] = status
    with open(path, "w") as app_file:
        yaml.dump(data, app_file, Dumper=yaml.SafeDumper)

    return


def get_app_scorenames(app_name: str) -> List[str]:
    """
    Function to get the score_names of the app and regitrer it
    This function requires to load the module and get the app
    names via a @staticmethod
    """
    app_dir = get_app_info(app_name)
    app_dir = Path(app_dir)

    sys.path.append(str(app_dir.parent))
    mod = importlib.import_module(app_name + ".src.app")
    scores = mod.App.score_names()
    # Remove last element of the path which was added manually
    sys.path.pop(-1)

    return scores


def get_configuration() -> Dict:
    """
    Get personal access token. User must use 'login' function at least once
    Get maximal file size can be uploaded.
    """
    path = Path.home().joinpath(".deep-chain").joinpath("config")
    if not path.is_file():
        raise ConfigNotFoundError

    with open(path, "r") as config_file:
        data = yaml.load(config_file, Loader=yaml.SafeLoader)
        data = {} if data is None else data

    return data


def _create_deechpain_folder() -> Path:
    """create .deepchain folder if not exist"""
    path = Path.home().joinpath(".deep-chain")
    path.mkdir(exist_ok=True)
    return path


def _create_config_file(root_path: Path) -> Path:
    """
    create the config file to store the personal access token
    """
    path = root_path.joinpath("config")
    path.touch(exist_ok=True)
    return path


def _create_apps_file(root_path: Path) -> Path:
    """
    create the apps file to store all the apps
    """
    path = root_path.joinpath("apps")
    path.touch(exist_ok=True)
    return path

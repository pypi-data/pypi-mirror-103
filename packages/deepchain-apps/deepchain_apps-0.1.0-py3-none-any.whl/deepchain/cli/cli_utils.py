"""Main functions used in CLI"""
import glob
import json
import os
import shutil
from typing import Dict, List

import requests
from deepchain import log


def upload_code(
    app_dir: str,
    app_name: str,
    pat: str,
    url: str,
    score_configuration: List[str],
) -> None:
    """Function to compress and upload code to google cloud bucket

    Args:
        app_dir (str): directory of the application code
        app_name (str): name of the application
        pat (str): personal token for uploading
        url (str): deployment URL
        score_configuration (List[str]): list of score names used in deepchain

    Returns:
        [type]: [description]
    """
    archive = shutil.make_archive(app_name, "tar", root_dir=app_dir + "/src")

    with open("scores.json", "w+") as config_file:
        json.dump(score_configuration, config_file)
    req = requests.post(
        url=url + app_name,
        headers={"authorisation": pat},
        files={
            "code": ("code.tar", open(archive, "rb"), "application/octet-stream"),
            "configuration": (
                "scores.json",
                open("scores.json", "rb"),
                "application/json",
            ),
            "tags": (
                "tags.json",
                open(app_dir + "/src/" + "tags.json", "rb"),
                "application/json",
            ),
            "description": (
                "description",
                open(app_dir + "/src/" + "DESC.md", "rb"),
                "application/text",
            ),
        },
    )

    os.remove(archive)
    os.remove("scores.json")
    return req


def upload_checkpoint(app_dir: str, app_name: str, pat: str, url: str, size_limit: int) -> None:
    """Tar checkpoints files and upload to deepchain

    Args:
        app_dir (str): directory of the application code
        app_name (str): name of the application
        pat (str): personal token for uploading
        url (str): deployment URL
        size_limit (int): size limit of the checkpoint

    Returns:
        [type]: [description]
    """
    signed_url = get_object_storage_url(app_name, pat, url)

    archive = shutil.make_archive(
        "checkpoint",
        "tar",
        app_dir + "/checkpoint",
    )
    if os.stat(archive).st_size / (1024 * 1024) > size_limit:
        print(f"Can not upload files over {size_limit}MB")
    else:
        req = requests.put(
            signed_url,
            data=open(archive, "rb").read(),
            headers={"Content-Type": "application/octet-stream"},
        )
    os.remove(archive)
    return req


def get_object_storage_url(app_name: str, pat: str, url: str) -> Dict:
    """
    Get the signed url to upload safely

    Args:
        app_name (str): application name
        pat (str): personnal token
        url (str): url of the API

    Returns:
        Dict: [description]
    """
    req = requests.post(url=url + app_name + "/checkpointUrl", headers={"authorisation": pat})
    signed_url = req.json()
    return signed_url


def fetch_latest_version() -> Dict:
    """
    Fetch info on last release version of the github repository.
    """
    url = "https://api.github.com/repos/instadeepai/deep-chain-apps/releases"
    req = requests.get(url)
    releases = req.json()
    latest_release = sorted(releases, key=lambda k: k["published_at"], reverse=True)[0]
    return latest_release


def download_latest_version(latest_release: Dict, temp_dir: str) -> None:
    """
    Function do downlad latest tarball image on github where templates are stored.
    repo link : https://github.com/instadeepai/deep-chain-apps

    Args:
        latest_release (Dict): Dictionnary with the latest release URL
        temp_dir (str): temporary folder to downlad tar file
    """
    log.info("downloading release  from : %s", latest_release["tarball_url"])
    req = requests.get(latest_release["tarball_url"])
    with open(f"{temp_dir}/{latest_release['tag_name']}.tar", "wb") as file:
        file.write(req.content)


def unpack_base_repository(dest_path: str, latest_release: Dict, temp_dir: str) -> None:
    """
    Function to unpack the github tar image download.
    Data are copied in a tmp folder

    Args:
        dest_path (str]): path to copy the files
        latest_release (Dict): dictionnary with release info
        temp_dir (str): [description]
    """
    shutil.unpack_archive(
        f"{temp_dir}/{latest_release['tag_name']}.tar",
        f"{temp_dir}/{latest_release['tag_name']}",
    )
    for file in glob.glob(rf"{temp_dir}/{latest_release['tag_name']}/*/**", recursive=True):
        shutil.copytree(file, dest_path)
        break

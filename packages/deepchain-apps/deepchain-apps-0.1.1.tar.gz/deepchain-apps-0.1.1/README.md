<p align="center">
  <img width="50%" src="./.source/_static/deepchain.png">
</p>

![PyPI](https://img.shields.io/pypi/v/deepchain-apps)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)

<details><summary>Table of contents</summary>

- [Description](#description)
- [Installation](#Installation)
- [Getting started with App](#usage)
- [CLI](#usage)
  - login
  - create
  - deploy
  - apps
- [Roadmap](#roadmap)
- [Citations](#citations)
- [License](#license)
</details>

# `deepchain-apps` : Create personnal app locally, deploy on deepchain.bio

This Package provide a **cli** for creating a personnal app to deploy on the DeepChain platform.
To leverage the apps capability, take a look at the [bio-transformers](https://pypi.org/project/bio-transformers/) and [bio-datasets](https://pypi.org/project/bio-datasets) package.

## Installation

You can install the package directly from Pypi:

```
pip install deepchain-apps
```

## Getting started with App

An application is a python folder that will be use on deepchain.bio platform to evaluate of protein.
The final app must have the following architecture:

### App structure

- my_application
  - src/
    - app.py
    - DESCRIPTION.md
    - tags.json
    - Optionnal : requirements.txt (for extra packages)
  - checkpoint/
    - Optionnal : model.[h5/pt]

The main app class must be named ’App’

### Tags
In order your app to be visible and well documented, tags should be filled to precised at least the *tasks* section.
  - tasks
  - librairies
  - embeddings
  - datasets

## CLI

The CLI provides 4 main commands:

- **login** : you need to supply the token provide on the plateform (PAT: personnal access token).

  ```
  deepchain login
  ```

- **create** : create a folder with a template app file

  ```
  deepchain create my_application
  ```

- **deploy** : the code and checkpoint are deployed on the plateform, you can select your app in the interface on the plateform.
  - with checkpoint upload

    ```
    deepchain deploy my_application --checkpoint
    ```

  - Only the code

    ```
    deepchain deploy my_application
    ```

- **apps** :
  - Get info on all local/upload apps

    ```
    deepchain apps --infos
    ```

  - Remove all local apps (files & config):

    ```
    deepchain apps --reset
    ```

  - Remove a specific application (files & config):

    ```
    deepchain apps --delete my_application
    ```

The application will be deploy in DeepChain plateform.

# Roadmap:

  - Synchronise apps with deepchain

# Citations

# License

This source code is licensed under the **Apache 2** license found in the `LICENSE` file in the root directory.

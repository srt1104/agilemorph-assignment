# Setup Instructions

## Basic Requirements
- VSCode Installation: Make sure you have [Visual Studio Code](https://code.visualstudio.com/) installed on your system.

- Docker Installation: Install [Docker](https://www.docker.com/) on your machine, as Dev Containers rely on Docker to create and manage containerized environments.

- VSCode Dev Containers Extension: Install the [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension from the VSCode marketplace. This extension allows VSCode to connect to and manage containers.

## Open and Start the Project

- Clone the [github repo](https://github.com/srt1104/agilemorph-assignment) on your local machine.

- Open VS Code and in the VS Code command pallette, search for the command "Dev Containers: Open Folder in Container..." and provide the path to the locally cloned repo.

- Once the devcontainer opens, run the following commands in the container terminal to get the project up and running:
    ```
    python init_db.py
    python seed_dp.py
    uvicorn app.main:app --reload
    ```

# Useful commands
- `python -m <module_name>.<file_name>`
- `pip freeze > requirements.txt`
- `pip install -r requirements.txt`
- `uvicorn app.main:app --reload`
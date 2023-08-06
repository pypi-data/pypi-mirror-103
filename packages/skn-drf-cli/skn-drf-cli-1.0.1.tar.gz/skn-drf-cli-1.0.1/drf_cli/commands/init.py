import click
import os
import platform

OPERATING_SYSTEM = platform.system()

def clone_repository(name):
    """
    Clones the reposity from git and removes the .git folder
    """

    repo_url = "https://github.com/shywn-mrk/drf-starter.git"

    command = f"git clone {repo_url} {name}"
    os.system(command)

    if OPERATING_SYSTEM == "Windows":
        os.system(f"rmdir /s /q \"{name}/.git\"")
    else:
        os.system(f"rm -rf {name}/.git")

def install_requirements(name):
    """
    Creates a virtual environment and installs the requirements
    """

    parent = os.getcwd()
    full_path = os.path.join(parent, name)
    os.chdir(full_path)
    os.system("python -m venv env")

    env_sub_dir = ""
    source = ""
    if OPERATING_SYSTEM == "Windows":
        env_sub_dir = "Scripts"
    else:
        env_sub_dir = "bin"
        source = ". "

    activate_file = os.path.join(full_path, "env", env_sub_dir, "activate")
    os.system(f"{source}{activate_file} && pip install -r requirements.txt")

@click.command()
@click.argument("name")
def cli(name):
    """
    Initialize a new Django Rest Framework project
    """

    try:
        clone_repository(name)

        install_requirements(name)

        print("Project has been initialized successfuly!")
    except:
        print("Something went wrong")

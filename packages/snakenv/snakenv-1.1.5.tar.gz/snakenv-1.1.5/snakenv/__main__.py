import os
import click
from os.path import isfile
from dotenv import dotenv_values


def add_to_global(key, value):
    os.environ[key] = value
    # from sys import platform
    # if platform in ["linux", "linux2", "darwin"]:
    #     os.system(f'export {key}="{value}"')
    # elif platform == "win32":
    #     os.system(f'set {key}="{value}"')


@click.command()
@click.argument("env_name", default="")
@click.option('--not-create', is_flag=True)
@click.option('--command','-c')
def main(env_name, not_create,command):
    env_file = env_name+(".env" if not ".env" in env_name else "")
    if isfile(env_file):
        env_data = dotenv_values(env_file)
        for key, value in env_data.items():
            add_to_global(key, value)
            print(f"[snakenv] {key} -> {value}")
        os.system(command)
    else:
        if not not_create:
            with open(env_file, "w") as f:
                f.write("")


def cli():
    try:
        main()
    except Exception as e:
        print("❌ "+str(e))

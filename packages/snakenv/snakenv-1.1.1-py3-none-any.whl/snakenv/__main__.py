import os
import click
from os.path import isfile
from dotenv import dotenv_values


@click.command()
@click.argument("env_name",default="")
def main(env_name):
    env_file = env_name+(".env" if not ".env" in env_name else "")
    if isfile(env_file):
        env_data = dotenv_values(env_file)
        for key, value in env_data.items():
            os.environ[key] = value
    else:
        with open(env_file, "w") as f:
            f.write("")


def cli():
    try:
        main()
    except Exception as e:
        print("❌ "+str(e))

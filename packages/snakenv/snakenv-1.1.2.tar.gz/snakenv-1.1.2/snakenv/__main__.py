import os
import click
from os.path import isfile
from dotenv import dotenv_values


@click.command()
@click.argument("env_name",default="")
@click.option('--not-create',is_flag=True)
def main(env_name,not_create):
    env_file = env_name+(".env" if not ".env" in env_name else "")
    if isfile(env_file):
        env_data = dotenv_values(env_file)
        for key, value in env_data.items():
            os.environ[key] = value
    else:
        if not not_create:
            with open(env_file, "w") as f:
                f.write("")


def cli():
    try:
        main()
    except Exception as e:
        print("❌ "+str(e))

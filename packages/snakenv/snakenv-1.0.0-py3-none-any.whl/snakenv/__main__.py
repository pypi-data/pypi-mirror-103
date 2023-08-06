import os
import click
from os.path import isfile
from dotenv import dotenv_values


@click.command()
@click.argument("cmd_arg")
def main(cmd_arg):
    env_name, filename = cmd_arg.split(":")
    env_file = env_name+(".env" if not ".env" in env_name else "")
    if isfile(env_file):
        env_data = dotenv_values(env_file)
        for key, value in env_data.items():
            os.environ[key] = value
        exec(open(filename).read())
    else:
        with open(env_file, "w") as f:
            f.write("")


def cli():
    try:
        main()
    except Exception as e:
        print("❌ "+str(e))

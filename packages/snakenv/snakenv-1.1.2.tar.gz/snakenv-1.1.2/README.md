# snakenv
**snakenv** is a command line application to make it possible to access variables in `.env` file as an environment variable in python script.

## Installation
For installing **snakenv** type:
```bash
> pip install snakenv
```

## Usage
You can use **snakenv** with following syntax:
```bash
> snakenv ENV_NAME
```
`ENV_NAME` is name of `env` file. You can enter file name with extension or it will use `.env` extension for default. Example, `prod` is equals `prod.env` and `prod.env` equals `prod.env`. 
If you leave ENV_NAME blank, it will use `.env` file.
If file not exist, it will create it. You can disable autocreate with `--not-create` flag.

### Thanks for using snakenv
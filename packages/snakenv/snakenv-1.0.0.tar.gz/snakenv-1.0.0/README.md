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
> snakenv ENV_FILE_NAME:PYTHON_FILE_NAME
```
You can also enter `ENV_FILE_NAME` without `.env` extension.
Example, for accessing environment variables from `x.env` file and run `y.py` file:
```bash
> snakenv x:y.py 
# or 
# snakenv x.env:x.py 
```
For using file with name of `.env` use can use:
```bash
> snakenv :PYTHON_FILE_NAME
```

### Thanks for using snakenv
# Python REST API wrapper for smarsy.ua website

This package provides REST API endpoints to work with smarsy.ua database.

# Run from sources

In order to run this app from sources you need following initial setup:
* Create new environment variable `SMARSY_PYTHON_INTERPRETER_PATH` with the path of the Python environment (venv). In windows you use something like `myvenv\Scripts\python.exe`
* Create `cfg/login.json` file and add `username`, `password` and `language` settings
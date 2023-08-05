# Installation instructions

## Clone the repository

```bash
$ git clone <LINK>
```

Copy the `<LINK>` of the repository.

## Prerequisites
1) Download Ubuntu packages

    ```bash
    $ sudo apt-get install -y git python3 python3-pip
    ```

2) Install virtual environment support

  ```bash
  $ pip3 install virtualenv --user
  ```

3) Install CaverDock & MGLTools following the instructions

## Install Python API
Run the following commands in the root directory of the project repository.

1) Create a virtual environment and use it. `<VENV>` is a placeholder for a name of virtual environment.

    ```bash
    $ virtualenv <VENV>
    $ source <VENV>/bin/activate
    ```

2) Install pycaverdock
    ```bash
   $ (<VENV>) pip3 install .
   ```

# Usage of Python API
Look at the pipeline example (`examples/pipeline.py`).

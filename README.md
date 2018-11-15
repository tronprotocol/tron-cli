# TRON-CLI
```
 _________  ____  _  __    _______   ____
/_  __/ _ \/ __ \/ |/ /___/ ___/ /  /  _/
 / / / , _/ /_/ /    /___/ /__/ /___/ /  
/_/ /_/|_|\____/_/|_/    \___/____/___/
```

A command line tool, to quick set up, turn on/off (multiple) tron nodes(full/solidity), and monitor running status.

* Learn more about tron on [TRON Developer Hub](https://developers.tron.network/docs/full-node)

* Join the community on [TRON Discord](https://discord.gg/GsRgsTD)

* Source code on [Github](https://github.com/tronprotocol/tron-cli)

## Install

### pip

> pip install --upgrade pip

```
pip install troncli
```

#### FAQs on installation

1. How to fix "fail to build a wheel for psutil" error?

    a. please check if you installed clang correctly, or install it using homebrew:

    ```
    brew install --with-toolchain llvm
    ```

    b. please check if you are using python 3.x

2. How to test in virtual environment?

    ```
    python3 -m venv venv
    ```

##### dev version:

```
pip install -i https://test.pypi.org/simple/ troncli
```

## Usage

| Command                                                                              | Functions                          | Example                                                                                                            |
|--------------------------------------------------------------------------------------|------------------------------------|--------------------------------------------------------------------------------------------------------------------|
| tron-cli quick                                                                       | Quick start.                       | tron-cli quick                                                                                                     |
| tron-cli init --version                                                              | Init dirs and fetch code.          | tron-cli init --version latest                                                                                     |
| tron-cli config --nettype --fullhttpport --solhttpport --fullgrpcport --solgrpcport  | Create and customize config files. | tron-cli config --nettype 'private' --fullhttpport 8500 --solhttpport 8600 --fullgrpcport 50051 --solgrpcport 5001 |
| tron-cli run --nodetype                                                              | Run node.                          | tron-cli run --nodetype full                                                                                       |
| tron-cli stop --pid                                                                  | Stop node.                         | tron-cli stop --pid 7777                                                                                           |
| tron-cli -h, --help                                                                  | Check help manual.                 | tron-cli -h                                                                                                        |


```
usage: cli.py [-h] {init,config,run,stop,quick} ...

which subcommand do you want?

optional arguments:
  -h, --help            show this help message and exit

subcommands:
  {init,config,run,stop,quick}
    init                Init dirs and fetch code. >> Settings: --version >>
    config              Customize config files. >> Settings: --nettype
                        --fullhttpport --solhttpport --fullgrpcport
                        --solgrpcport
    run                 Run nodes. >> Settings: --nodetype
    stop                Stop nodes. >> Settings: --pid
    quick               Quick start. (run a full private node by one command)
                        >> Example: tron-cli quick
```

## Dev List

[ ] run - monitor running nodes

[ ] run - filter nodes

[ ] run - multiple (full) nodes

[ ] dump - fetch a dump

[ ] CLI UI imporve

[ ] init - add option to build from source code

##### Version 0.1.0

[X] init - set up file folders, and get builds based on given version number

[X] config - init basic config file in json format, and convert to java properties format and export

[X] run - run a single main net full node

[X] quick start

[X] run - move 'run' to its handler, and async the call 

[X] stop - add sub cmd and its handler to stop all nodes (kill -15)

[X] run - change log and data store location

[X] config - add custom method to fire up private/shasta testnet

[X] config - add custom method to change port number

[X] config - add custom method to fire up solidity node

[X] run - add option to run solidity node

[X] pack to pip

[X] Doc - add more instruction in readme file

# <img src="./doc/logo.png" alt="logo" width="50"/> TRON-CLI

A command line tool, to quickly set up, manage TRON nodes(full/solidity), and monitor running status.

```
 _________  ____  _  __    _______   ____
/_  __/ _ \/ __ \/ |/ /___/ ___/ /  /  _/
 / / / , _/ /_/ /    /___/ /__/ /___/ /  
/_/ /_/|_|\____/_/|_/    \___/____/___/
```

| Python | JDK |
|--------|-----|
| 3.6+   | Oracle 1.8 |

* Learn more about tron on [TRON Developer Hub](https://developers.tron.network/docs/full-node)

* Join the community on [TRON Discord](https://discord.gg/GsRgsTD)

* Source code on [Github](https://github.com/tronprotocol/tron-cli)

* Project on [Pypi](https://pypi.org/project/troncli/)

------

## Install

### pip

> pip install --upgrade pip

```
pip install troncli
```

------

## Usage

### Interactive Mode

```
tron-cli i
```

Quickly set up what you want by answerinig few questions.

![gif](./doc/imode.gif)

### Quick Command

```
tron-cli quick
```

By default, it will set up a private test-net full node for you. 

* You can also ```--nettype main``` to choose set up a full node sync to main net.

* ```--reset True``` to reset all

![gif](./doc/quick.gif)

### Advanced Set up

You can set up full node, solidity node, event node and grid api service (local tron-grid) with more detailed receipt by provided subcommands. See usage by ```tron-cli -h```, and ```-h``` on each subcommands.

#### Manual 

| Command                                                                                                                                                                                                                            | Functions                          | Example1         | Example2                                                                                                                                                                                                                                                                                                                        |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------|------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| tron-cli init --version --reset                                                                                                                                                                                                    | Init dirs and fetch code.          | tron-cli init    | tron-cli init --version 3.2.2 --reset True                                                                                                                                                                                                                                                                                      |
| tron-cli config --nettype ---nettype --fullhttpport --solhttpport --eventhttpport --fullrpcport --solrpcport --eventrpcport --enablememdb --dbsyncmode --saveintertx --savehistorytx --gridport --dbname --dbusername --dbpassword | Create and customize config files. | tron-cli config  | tron-cli config --nettype private --fullhttpport 8500 --solhttpport 8600 --eventhttpport 8400 --fullrpcport 58500 --solrpcport 58600 --eventrpcport 58400 --enablememdb True --dbsyncmode async --saveintertx False --savehistorytx False --gridport 18891 --dbname events --dbusername tron --dbpassword 12345678 --reset True |
| tron-cli run --nodetype                                                                                                                                                                                                            | Run node.                          | tron-cli run     | tron-cli run --nodetype full                                                                                                                                                                                                                                                                                                    |
| tron-cli stop --node                                                                                                                                                                                                               | Stop node.                         | tron-cli stop    | tron-cli stop --node 7777                                                                                                                                                                                                                                                                                                       |
| tron-cli status --node                                                                                                                                                                                                             | Monitor nodes status.              | tron-cli status  | tron-cli status --node 777                                                                                                                                                                                                                                                                                                      |
| tron-cli quick --reset                                                                                                                                                                                                             | Quick start.                       | tron-cli quick   | tron-cli quick --nettype main --reset True                                                                                                                                                                                                                                                                                      |
| tron-cli log --nodetype --filter                                                                                                                                                                                                   | Show filtered log.                 | tron-cli log     | tron-cli --nodetype sol --filter height                                                                                                                                                                                                                                                                                         |
| tron-cli i                                                                                                                                                                                                                         | Switch to Interactive Mode.        | tron-cli i       | tron-cli i                                                                                                                                                                                                                                                                                                                      |
| tron-cli version                                                                                                                                                                                                                   | Check installed troncli version.   | tron-cli version | tron-cli version                                                                                                                                                                                                                                                                                                                |
| tron-cli -h, --help                                                                                                                                                                                                                | Check help manual.                 | tron-cli -h      | tron-cli --help                                                                                                                                                                                                                                                                                                                 |

#### overall

```
tron-cli -h
```
```
usage: tron-cli [-h] {init,config,run,stop,status,quick,log,version,i} ...

which subcommand do you want?

optional arguments:
  -h, --help            show this help message and exit

subcommands:
  {init,config,run,stop,status,quick,log,version,i}
    init                Init dirs and fetch code.
    config              Create customize config files.
    run                 Run node.
    stop                Stop node.
    status              Monitor nodes status.
    quick               Quick start. (run a full private/main node by one
                        command)
    log                 Show filtered log.
    version             Check installed troncli version.
    i                   Interactive Mode.
```

##### subcommand: init

```
tron-cli init -h
```
```
usage: tron-cli init [-h] [--version VERSION] [--reset RESET]

optional arguments:
  -h, --help         show this help message and exit
  --version VERSION  specify java-tron version
  --reset RESET      reset all
```

##### subcommand: config

```
tron-cli config -h
```
```
usage: tron-cli config [-h] [--nettype NETTYPE] [--fullhttpport FULLHTTPPORT]
                       [--solhttpport SOLHTTPPORT]
                       [--eventhttpport EVENTHTTPPORT]
                       [--fullrpcport FULLRPCPORT] [--solrpcport SOLRPCPORT]
                       [--eventrpcport EVENTRPCPORT]
                       [--enablememdb ENABLEMEMDB] [--dbsyncmode DBSYNCMODE]
                       [--saveintertx SAVEINTERTX]
                       [--savehistorytx SAVEHISTORYTX] [--gridport GRIDPORT]
                       [--dbname DBNAME] [--dbusername DBUSERNAME]
                       [--dbpassword DBPASSWORD] [--reset RESET]

optional arguments:
  -h, --help            show this help message and exit
  --nettype NETTYPE     specify net type [main, private]
  --fullhttpport FULLHTTPPORT
                        specify full node http port
  --solhttpport SOLHTTPPORT
                        specify solidity node http port
  --eventhttpport EVENTHTTPPORT
                        specify event node http port
  --fullrpcport FULLRPCPORT
                        specify full node rpc port
  --solrpcport SOLRPCPORT
                        specify solidity node rpc port
  --eventrpcport EVENTRPCPORT
                        specify event node rpc port
  --enablememdb ENABLEMEMDB
                        enable/disable in memory db
  --dbsyncmode DBSYNCMODE
                        specify either db async or sync mode
  --saveintertx SAVEINTERTX
                        enable/disable save internal transcation
  --savehistorytx SAVEHISTORYTX
                        enable/disable save history transcation
  --gridport GRIDPORT   specify grid api port
  --dbname DBNAME       specify db name
  --dbusername DBUSERNAME
                        specify db user name
  --dbpassword DBPASSWORD
                        specify db password name
  --reset RESET         reset config to default settings
```

##### subcommand: run

```
tron-cli run -h
```
```
usage: tron-cli run [-h] [--nodetype NODETYPE]

optional arguments:
  -h, --help           show this help message and exit
  --nodetype NODETYPE  specify node type [full, sol, event, grid]
```

##### subcommand: stop

```
tron-cli stop -h
```
```
usage: tron-cli stop [-h] [--node NODE]

optional arguments:
  -h, --help   show this help message and exit
  --node NODE  stop node by given node id or all
```

##### subcommand: status

```
tron-cli status -h
```
```
usage: tron-cli status [-h] [--node NODE]

optional arguments:
  -h, --help   show this help message and exit
  --node NODE  check specific node detail by node id
```

##### subcommand: log

```
tron-cli log -h
```
```
usage: tron-cli log [-h] [--nodetype NODETYPE] [--filter FILTER]

optional arguments:
  -h, --help           show this help message and exit
  --nodetype NODETYPE  specify node type [full, sol, event, grid]
  --filter FILTER      specify filter [number/height]
```

##### subcommand: version

```
tron-cli version -h
```
```
usage: tron-cli version [-h]

optional arguments:
  -h, --help  show this help message and exit
```

##### subcommand: i

```
tron-cli i -h
```
```
usage: tron-cli i [-h]

optional arguments:
  -h, --help  show this help message and exit
```

------

## Common Use Cases

__Notice__: Take a look at ```tron-cli i``` first, interactive mode should cover most use cases.

#### I. set up private-net nodes

a. set up full node only

```
tron-cli quick
```

b. add a solidity node

```
tron-cli run --nodetype sol
```

#### II. set up main-net nodes

a. init

```
tron-cli init
```

b. config to main-net

```
tron-cli config --nettype main
```

c. run full node

```
tron-cli run
```

#### III. advanced config to start nodes

a. initilize

```
tron-cli init --version latest --reset True
```

b. detail config (specify parameter to overwrite default)

```
tron-cli config --nettype private --fullhttpport 8500 --solhttpport 8600 --eventhttpport 8400 --fullrpcport 58500 --solrpcport 58600 --eventrpcport 58400 --enablememdb True --dbsyncmode async --saveintertx False --savehistorytx False --gridport 18891 --dbname Null --dbusername Null --dbpassword Null
```

c. run full/sol

```
tron-cli run --nodetype full
```

#### IV. start private full node + event node + tron-grid

a. install mongodb and create user & db

b. initilize

```
tron-cli init
```

c. config (specify parameter to overwrite default) __dbname dbusername dbpassword are required to set__

```
tron-cli config --nettype private --fullhttpport 8500 --solhttpport 8600 --eventhttpport 8400 --fullrpcport 58500 --solrpcport 58600 --eventrpcport 58400 --enablememdb True --dbsyncmode async --saveintertx False --savehistorytx False --gridport 18891 --dbname events --dbusername tron --dbpassword 12345678
```

d. run full node

```
tron-cli run
```

e. run event node

```
tron-cli run --nodetype event
```

f. run tron-grid

```
tron-cli run --nodetype grid
```

#### V. start mainnet event node + tron-grid

a. install mongodb and create user & db

b. initilize

```
tron-cli init
```

c. config (specify parameter to overwrite default) __dbname dbusername dbpassword are required to set__

```
tron-cli config --nettype main --fullhttpport 8500 --solhttpport 8600 --eventhttpport 8400 --fullrpcport 58500 --solrpcport 58600 --eventrpcport 58400 --enablememdb True --dbsyncmode async --saveintertx False --savehistorytx False --gridport 18891 --dbname events --dbusername tron --dbpassword 12345678
```

d. run event node

```
tron-cli run --nodetype event
```

e. run tron-grid

```
tron-cli run --nodetype grid
```

------

## FAQs on installation

1. How to fix "fail to build a wheel for psutil" error?

    a. please check if you installed clang correctly, or install it using homebrew:

    ```
    brew install --with-toolchain llvm
    ```

    b. please check if you are using python 3.x

2. How to test in virtual environment?
    
    a. create virtual environment

    ```
    python3 -m venv venv
    ```

    b. activate venv

    ```
    . ./venv/bin/activate
    ```

    c. install troncli in venv

    ```
    pip install troncli
    ```

    d. when done testing, or using the venv - to deactivate venv

    ```
    deactivate
    ```

![logo](./doc/logo.png)

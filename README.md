# tron-cli
```
 _________  ____  _  __    _______   ____
/_  __/ _ \/ __ \/ |/ /___/ ___/ /  /  _/
 / / / , _/ /_/ /    /___/ /__/ /___/ /  
/_/ /_/|_|\____/_/|_/    \___/____/___/
```

## Purposes

Provide a command line tool, to quick set up, turn on/off (multiple) tron nodes(full/solidity), and monitoring them.

__Coming Soon__

#### It's not complete yet

well, if you really want to try it now:

```
python ../tron-cli/cli.py quick
```

## Dev List

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

[ ] Doc - add more instruction in readme file

[ ] run - monitor running nodes

[ ] run - filter nodes

[ ] run - multiple (full) nodes

[ ] dump - fetch a dump

[ ] CLI UI imporve

[ ] init - add option to build from source code
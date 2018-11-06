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

[ ] run - move 'run' to its handler, and async the call 

[ ] stop - add sub cmd and its handler to stop all nodes (kill -15)

[ ] config - change log and data store location

[ ] Doc - add more instruction in readme file

[ ] pack to pip

[ ] config - add custom method to fire up private/shasta testnet

[ ] config - add custom method to change port number

[ ] config - add custom method to fire up solidity node

[ ] run - add option to run solidity node

[ ] run - monitor running nodes

[ ] run - filter nodes

[ ] run - multiple (full) nodes

[ ] dump - fetch a dump

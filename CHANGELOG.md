# Changelog

### Dev Pipeline

[ ] quick - add options to start common user cases

[ ] restart - restart all running nodes

[ ] clean up all std messages

[ ] config - set default/customize committee proposal list

[ ] log - show and filter nodes log

[ ] dump - fetch a dump

[ ] db - manage db, check and trim db

[ ] manual - add more instruction for config

[ ] interact - add interactive mode

[ ] quiet - add quiet mode

[ ] run - multiple (full) nodes

[blocked] config -- add option to config to sync with newly deployed shasta testnet

#### Version 0.3.0

##### highlight:

* Redesign config logic and provide more features.

* Set up mongodb with a default setting.

##### details:

[X] Redesign config logic check and restore previous config settings. Only overwrite by given options.tron

[X] add config -- reset: reset to default config

[ ] db - mongodb create db and set user name, user role, db name, and psd

[ ] version - show current and also check latest version


#### Version 0.2.4

[X] Fix get current node status async error.

#### Version 0.2.3

[X] Catch more errors.

#### Version 0.2.2

[X] Fix [issue#17](https://github.com/tronprotocol/tron-cli/issues/17)

[X] check java install and JDK version

[X] check python version

[X] check git install

[X] status - display recommended cpu / mem for running full nodes

[X] status & run - display log locations

[X] init & status - store and display java-tron node versions

[X] status - show test account/witness's private key and address for private net

#### Version 0.2.1

[X] store config, and show active config cmd in status

[X] provide connection info in status

[X] add --reset for quick

[X] add more instruction in command

[X] show ports info and cmd tips with run command

#### Version 0.2.0

##### highlight:

Support event-node and tron-grid set up/config/run/stop/monitor.

##### details:

[X] support java-tron 3.2.2 with more config

[X] add stop all feature

[X] update logo and change node list structure

[X] fix private net init account pk and address does not match

#### Version 0.1.6

[X] fix error on download progress bar when network not available

#### Version 0.1.5

##### highlight:

Pre-release of support event-node and tron-grid set up/config/run/stop/monitor.

##### details:

[X] init - change file structure for event-node and tron-grid

[X] init - add reset option and handler

[X] init - fetch event-node code

[X] init - fetch tron-grid code

[X] utils - make git_clone a util function

[X] utils - build util method to store more info and provide for status

[X] config - add options and handlers for event-node

[X] config - add options and handlers for tron-grid

[X] config - add event-node build and raise errors

[X] run - add event-node run

[X] run - fire up tron-grid

#### Version 0.1.4

[X] update to support version 3.2 fetch release, check version

[X] compatible check with version 3.2 release, and update config handler

[X] add more info message;

[X] provide a more neat yet detail help info and command

#### Version 0.1.3

[X] run - check single ps status

[X] keep track of all running nodes

[X] run - monitor overall system status

[X] set default value for all subcommand options

#### Version 0.1.2

[X] catch download errors

[X] add progress bar for download

[X] colorful logo and msg

[X] add more progress msg on ports config

[X] add more progress msg on net_type config

[X] add info msg type for instructions

[X] move changelog to file

[X] optimize progress bar

#### Version 0.1.0

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
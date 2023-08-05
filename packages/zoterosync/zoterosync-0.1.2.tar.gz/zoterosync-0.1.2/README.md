# Zoterosync

Syncs local zotero files to a remote storage using rclone. This is a work in progress.

## Software requirements
  * python 3
  * pip 
  * [rclone](https://rclone.org/)
  * [virtualenv](https://virtualenv.pypa.io/en/latest/): virtual environment is apropriated to install compatible dependencies
  * bash

## Recomended software
  * Linux Distro: not tested on other platforms
  * Google Drive: rclone is compatible with a lot of cloud storage, but we've tested only with 'drive' option.

## Install zoterosync
<!-- 
  * Download the [last release available](https://gitlab.com/marceloakira/zoterosync/-/releases)
    * Suppose you downloaded [v0.1.0 release packaged with zip](https://gitlab.com/marceloakira/zoterosync/-/archive/v0.1.0/zoterosync-v0.1.0.zip)
  * Uncompress your package with your preferred software or execute this command line:
```bash
unzip  zoterosync-v0.1.0.zip
```  
-->
  * Download the latest version with git:
```bash
git clone https://gitlab.com/marceloakira/zoterosync
```
  * Create a virtual environment with python3 as default interpreter:
```bash
virtualenv --python=python3 zoterosync
```
  * Install required python libraries inside virtual environment:
```bash
cd zoterosync
source bin/activate
pip install -r requirements.txt
```
  * Create configuration:
```bash
# generates default configuration
python zoterosync_cli.py config
```
  * Setup script:
```bash
# create a directory for executable scripts
mkdir -P ~/bin
# add this path to PATH environment variable
echo "~/bin" >> ~/.profile
# setup script
ln -s $PWD/zoterosync.bash ~/bin/zoterosync
# close the current terminal and test command
zoterosync
```

## Configure a remote storage
```
$ rclone config
Current remotes:

Name                 Type
====                 ====

e) Edit existing remote
n) New remote
d) Delete remote
r) Rename remote
c) Copy remote
s) Set configuration password
q) Quit config
e/n/d/r/c/s/q> n
name> Quantum Computing
Type of storage to configure.
Enter a string value. Press Enter for the default ("").
Choose a number from below, or type in your own value
...
13 / Google Drive
   \ "drive"
...
Storage>13 
* See help for drive backend at: https://rclone.org/drive/ **

Google Application Client Id
Setting your own is recommended.
See https://rclone.org/drive/#making-your-own-client-id for how to create your own.
If you leave this blank, it will use an internal key which is low performance.
Enter a string value. Press Enter for the default ("").
client_id>      <--- press Enter
OAuth Client Secret
Leave blank normally.
Enter a string value. Press Enter for the default ("").
client_secret>     <--- press Enter
Scope that rclone should use when requesting access from drive.
Enter a string value. Press Enter for the default ("").
Choose a number from below, or type in your own value
 1 / Full access all files, excluding Application Data Folder.
   \ "drive"
...
scope> 1 
ID of the root folder
Leave blank normally.

Fill in to access "Computers" folders (see docs), or for rclone to use
a non root folder as its starting point.

Enter a string value. Press Enter for the default ("").
root_folder_id>       <--- press Enter
Service Account Credentials JSON file path 
Leave blank normally.
Needed only if you want use SA instead of interactive login.

Leading `~` will be expanded in the file name as will environment variables such as `${RCLONE_CONFIG_DIR}`.

Enter a string value. Press Enter for the default ("").
service_account_file>  <--- Press Enter
Edit advanced config? (y/n)
y) Yes
n) No (default)
y/n>      <-- press Enter
Use auto config?
 * Say Y if not sure
 * Say N if you are working on a remote or headless machine
y) Yes (default)
n) No
y/n>     <-- press Enter
If your browser doesn't open automatically go to the following link: http://127.0.0.1:53682/auth?state=WOqyzeguK5dtqpDkDnplOQ
Log in and authorize rclone for access
Waiting for code...      <-- configuration with browser
Log in and authorize rclone for access
Waiting for code...
Got code
Configure this as a team drive?
y) Yes
n) No (default)
y/n> y
Fetching team drive list...
Choose a number from below, or type in your own value
...
  3 / Quantum Computing
   \ "0ABtgQWBCM1GiUk9PVA"
...
[Quantum Computing]
type = drive
scope = drive
token = {xxx}
team_drive = 0AIZzmLgyr5CaUk9PVA
root_folder_id = 
--------------------
y) Yes this is OK (default)
e) Edit this remote
d) Delete this remote
y/e/d> y
```

## List your groups and set a remote
```bash
$ zoterosync listremotes
quantum-computing
$ zoterosync listgroups
Quantum Computing
$ zoterosync setremote 'Quantum Computing' 'quantum-computing'
creating remote path quantum-computing:zotero-storage
remote path created
```
## List your groups in local storage and push
```bash
$ zoterosync push 'Quantum Computing'
...
2020/12/25 11:50:43 INFO  : 
Transferred:       19.321M / 19.321 MBytes, 100%, 282.299 kBytes/s, ETA 0s
Transferred:           34 / 34, 100%
Elapsed time:      1m12.2s
```
## List your remotes and pull
```bash
$ zoterosync listremotes
Quantum Computing
$ zoterosync pull 'Quantum Computing'
pulling changed files from remote to local storage
2020/12/25 11:53:53 INFO  : There was nothing to transfer
2020/12/25 11:53:53 INFO  : 
Transferred:             0 / 0 Bytes, -, 0 Bytes/s, ETA -
Checks:                34 / 34, 100%
Elapsed time:         3.5s
...
```

That's it, enjoy zoterosync!
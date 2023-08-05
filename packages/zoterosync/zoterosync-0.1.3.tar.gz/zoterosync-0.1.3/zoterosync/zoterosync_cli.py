"""Command line interface (CLI) for ZoteroSync"""
import os
import json
import click
from .zoterosync import ZoteroSync
from dotenv import load_dotenv
load_dotenv()

home_dir = os.path.expanduser('~')
zotero_path = home_dir+'/Zotero'
zoterosync_path = None
if os.getenv('ZOTEROSYNC_HOME') is None:
    zoterosync_path = home_dir+'/.zoterosync'
else:
    zoterosync_path = './.zoterosync'    

zotero_sync = ZoteroSync(zotero_path, zoterosync_path)

@click.group()
def cli():
  """sync zotero storage with a rclone remote"""

@cli.command(short_help='push changed files from zotero group to remote')
@click.argument('group_name', type=str, required=False)
@click.option('--all', '-a', required=False, is_flag=True, help='push all groups')
def push(group_name, all):
  """push changes from GROUP_NAME local storage to remote 
  
  EXAMPLE:\n
        Push changes in 'quantum computing' group from local zotero storage to remote:\n
        $ zoterosync push 'Quantum Computing'\n
        You can configure a remote to a group with 'setremote' command.\n
        \n
        You can push all groups with remotes with all flag:\n
        $ zoterosync push -a\n
        This flag is True as default value 
  """
  if group_name is None:
    groups = zotero_sync.list_groups_with_remote()
    for group_name in groups.keys():
      print('Pushing modified files from '+group_name+' group:')
      sync_dir = zotero_sync.link_files(group_name)
      remote_dir = zotero_sync.remote_dir(group_name)
      zotero_sync.copy_files(sync_dir, remote_dir)
      print('Finished pushing files from '+group_name+' group')
  else:
    sync_dir = zotero_sync.link_files(group_name)
    remote_dir = zotero_sync.remote_dir(group_name)
    zotero_sync.copy_files(sync_dir, remote_dir)

@cli.command(short_help='pull changed files from remote to local storage')
@click.argument('group_name', type=str, required=False)
@click.option('--all', '-a', required=False, is_flag=True, default=True, help='pull all groups')
def pull(group_name,all):
  """pull changed files from remote to local storage of GROUP_NAME
  
  EXAMPLE:\n
        You can pull changed files from 'Quantum Computing' remote with this command line:\n
        $ zoterosync pull 'Quantum Computing'\n
        You can configure a remote to a group with 'setremote' command.\n
        \n
        You can pull all groups with remotes with all flag:\n
        $ zoterosync pull -a\n
        This flag is True as default value 
  """
  local_storage = zotero_sync.local_storage()
  if group_name is None:
    groups = zotero_sync.list_groups_with_remote()
    for group_name in groups.keys():
      print('Pushing modified files from '+group_name+' group:')
      remote_dir = zotero_sync.remote_dir(group_name)
      zotero_sync.copy_files(remote_dir, local_storage)
      print('Finished pulling files from '+group_name+' group')
  else:
    remote_dir = zotero_sync.remote_dir(group_name)
    zotero_sync.copy_files(remote_dir, local_storage)

@cli.command(short_help='list groups from zotero')
def listgroups():
  """list groups from zotero
  
  \b
  EXAMPLE:
      $ zoterosync listgroups
      Quantum Computing
      Argument Mining

      Zotero is current configured with 'Quantum Computing' and 'Argument Mining' groups.\n
      Obs.: Due to database locking, you can only execute this command if Zotero is closed.\n
  """
  groups = zotero_sync.list_groups_from_sqlite()
  for group in groups:
    print(group)

@cli.command(short_help='list remotes from rclone')
def listremotes():
  """list remotes from rclone

  \b
  EXAMPLE:
      $ zoterosync listremotes
      quantum-computing
      argument-mining
  
      You can config remotes with 'rclone config'
  """
  print(zotero_sync.list_remotes().rstrip())

@cli.command(short_help='show config')
def config():
  """show config in JSON format
  
  \b
  EXAMPLE:
      $ zoterosync config

      JSON format is used to configuration file, you can manually edit if you want.\n
  """
  config = zotero_sync.load_config()
  print(json.dumps(config,indent=1))

@cli.command(short_help='set remote to a zotero group')
@click.argument('group_name', type=str)
@click.argument('remote', type=str)
def setremote(group_name, remote):
  """set REMOTE to group identified by GROUP_NAME

  \b
  EXAMPLE:
      Set remote 'quantum-computing' to 'Quantum Computing' group:      
      $ zoterosync setremote 'Quantum Computing' 'quantum-computing'
  """
  zotero_sync.setremote(group_name, remote)

def main():
    cli()
    
if __name__ == '__main__':
    cli()

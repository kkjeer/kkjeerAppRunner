import logging
import os
import json

from installed_clients.WorkspaceClient import Workspace

# This class is responsible for reading and writing files to the user's workspace.
class FileUtil:
  def __init__(self, config):
    self.config = config
    self.callback_url = os.environ['SDK_CALLBACK_URL']
    self.ws_url = config["workspace-url"]
    self.shared_folder = config['scratch']
    logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                        level=logging.INFO)
    
  def readFBAOutputs(self, ctx, refs):
    try:
      ws = Workspace(self.ws_url, token=ctx['token'])
      to_read = [{'ref': ref} for ref in refs]
      obj = ws.get_objects2({'objects': to_read})
      print(f'read fba outputs: {json.dumps(obj, indent=2)}')
      return obj
    except Exception as e:
      print(f'count not read fba outputs: {e}')
      return None
    
  # This method demonstrates reading the string table that was created at the end of running this app
  # (this might be a useful reference for the later app that reads the table)
  def readStringTable(self, ctx):
    try:
      ws = Workspace(self.ws_url, token=ctx['token'])
      ref = '76795/89/8'
      obj = ws.get_objects2({'objects' : [{'ref' : ref}]})
      print(f'read string table: {obj}')
      return obj
    except Exception as e:
      print(f'could not read string table: {e}')
      return None

  # This method writes the results of the fba runs into a string data table
  # so that other apps can read this data and ask the user for input based on the results.
  def writeStringTable(self, ctx, params, tableData):
    try:
      ws = Workspace(self.ws_url, token=ctx['token'])
      save_result = ws.save_objects(
         {
           'workspace': params['workspace_name'],
           'objects': [
              {
                'name': 'app-runner-table',
                'type': 'MAK.StringDataTable',
                'data': tableData,
              }
            ]
          })
      print(f'string data table: {save_result}')
      id = save_result[0][0]
      version = save_result[0][4]
      workspace_id = save_result[0][6]
      ref = f'{workspace_id}/{id}/{version}'
      return {'ref': ref, 'description': 'summary of results'}
    except Exception as e:
      print(f'failed to save string data table: {e}')
      return None
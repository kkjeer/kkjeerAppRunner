# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
import json

from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.KBParallelClient import KBParallel
from installed_clients.WorkspaceClient import Workspace
#END_HEADER


class kkjeerAppRunner:
    '''
    Module Name:
    kkjeerAppRunner

    Module Description:
    A KBase module: kkjeerAppRunner
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "https://github.com/kkjeer/kkjeerAppRunner"
    GIT_COMMIT_HASH = "13602ad92e5e0a28bdab3cf9a31a460a3914f15b"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.ws_url = config["workspace-url"]
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        #END_CONSTRUCTOR
        pass


    def run_kkjeerAppRunner(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_kkjeerAppRunner
        print('Starting AppRunner run function')

        # Experiment with reading the string table created during one of the previous app runs
        self.readStringTable(ctx)
        
        # Run the FBA app using KBParallel
        tasks = self.createTasks(params)
        kbparallel_result = self.runKBParallel(tasks)

        # Set of objects created during this app run (will be linked to in the report at the end)
        objects_created = []

        # Use the task parameters and the KBParallel results to construct
        # the data that will be used in the output file, and
        # the HTML summary text that will be used in the report
        tableData = {
          'row_ids': [],
          'column_ids': [],
          'row_labels': [],
          'column_labels': [],
          'row_groups_ids': [],
          'column_groups_ids': [],
          'data': []
        }

        # Top row of summary table: parameters used in each fba run and the results of the run
        summary = "<table>"
        summary += "<tr>"
        param_names = list(tasks[0]['parameters'].keys())
        param_names = [item for item in param_names if item != "workspace"]
        table_headers = param_names + ['objective value', 'result ref']
        for h in table_headers:
          summary += f'<th style="padding: 5px">{h}</th>'
        summary += "</tr>"

        tableData['column_ids'] = table_headers
        tableData['column_labels'] = table_headers

        # Fill in the rows of the table data and summary table text
        for i in range(0, len(tasks)):
          tableData['row_ids'].append(f'row{i}')
          tableData['row_labels'].append(f'row {i}')
          t = tasks[i]
          p = t['parameters']
          r = kbparallel_result['results'][i]['final_job_state']['result'][0]
          objective = r['objective']
          new_fba_ref = r['new_fba_ref']
          summary += "<tr style=\"border-top: 1px solid #505050;\">"
          data = []
          bg = "#f4f4f4" if i % 2 == 1 else "transparent"
          style = f'style="padding: 5px; background-color: {bg};"'
          for name in param_names:
            summary += f'<td {style}">{p[name]}</td>'
            data.append(str(p[name]))
          summary += f'<td {style}>{objective}</td>'
          summary += f'<td {style}>{new_fba_ref}</td>'
          summary += "</tr>"
          tableData['data'].append(data)
          objects_created.append({'ref': new_fba_ref, 'description': f'results of running fba configuration {i}'})
        summary += "</table>"

        # Save the results into a string data table
        # (if successful, this will be another object linked to in the final report)
        string_data_table = self.writeStringTable(ctx, params, tableData)
        if string_data_table is not None:
          objects_created.append(string_data_table)

        # Extra message to help debug (optionally append to the text_message in the report below)
        debug_message = f'<p>Params: {params["param_group"]}</p><p>Tasks: {tasks}</p><p>All params: {json.dumps(params, indent=2)}</p><p>KBParallel result:</p><pre>{json.dumps(kbparallel_result, indent=2)}</pre>'

        # Create the output report
        report = KBaseReport(self.callback_url)          
        report_info = report.create(
          {
            'report': {
              'objects_created': objects_created,
              'text_message': f'{summary}<br />{debug_message}'
            },
            'workspace_name': params['workspace_name']
          }
        )
        output = {
            'report_name': report_info['name'],
            'report_ref': report_info['ref'],
        }
        #END run_kkjeerAppRunner

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_kkjeerAppRunner return value ' +
                             'output is not type dict as required.')
        # return the results
        return []
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
    
    # This method uses the parameters the user entered in the app to create a set of tasks to pass to KBParallel.
    # The only app allowed (currently) is fba_tools.run_flux_balance_analysis.
    # This is because KBase currently doesn't support dynamic UI, so this means
    # the spec.json file can include only the parameters supported by fba_tools.run_flux_balance_analysis,
    # and because fba_tools.run_flux_balance_analysis doesn't internally call KBParallel. Other apps that
    # do can lead to exploding KBParallel calls and overwhelm the KBase system.
    # Currently, spec.json only contains a subset of the parameters supported by run_flux_balance_analysis;
    # more can be added by looking at the spec.json file from the run_flux_balance_analysis GitHub.
    def createTasks(self, params):
      
      tasks = [
        {
          'module_name': 'fba_tools',
          'function_name': 'run_flux_balance_analysis',
          'version': 'release',
          'parameters': {
            'fba_output_id': f'apprunner-fba-output-{i}',
            'target_reaction': '4HBTE_c0',
            **params['param_group'][i],
            'workspace': params['workspace_name']
          }
        }
        for i in range(0, len(params["param_group"]))
      ]
      print(f'Tasks: {tasks}')
      return tasks
    
    # This method runs KBParallel on the given set of tasks.
    def runKBParallel(self, tasks):
      # Configure how KBParallel should run.
      # Note that KBParallel is not a supported app. There is currently no supported way
      # to run other apps from within a KBase app; KBParallel is only used as a way to
      # demonstrate the proposed workflow of the test runner app.
      batch_run_params = {
        'tasks': tasks,
        'runner': 'parallel',
        'concurrent_local_tasks': 1,
        'concurrent_njsw_tasks': 2,
        'max_retries': 2
      }
      
      # Run the tasks
      parallel_runner = KBParallel(self.callback_url)
      result = parallel_runner.run_batch(batch_run_params)
      return result
    
    # This method demonstrates reading the string table that was created at the end of running this app
    # (this might be useful for the later app that reads the table)
    def readStringTable(self, ctx):
      try:
        ws = Workspace(self.ws_url, token=ctx['token'])
        ref = '76795/89/8'
        obj = ws.get_objects2({'objects' : [{'ref' : ref}]})
        print(f'read string table: {obj}')
      except Exception as e:
        print(f'could not read string table: {e}')

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

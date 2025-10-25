# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
import json

from installed_clients.KBaseReportClient import KBaseReport

from Utils.AppRunnerUtil import AppRunnerUtil
from Utils.FileUtil import FileUtil
from Utils.OutputUtil import OutputUtil
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
        self.config = config
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
        logging.info('Starting AppRunner run function')

        # Create utilities
        runner = AppRunnerUtil(self.config)
        fileUtil = FileUtil(self.config)
        outputUtil = OutputUtil(self.config)

        # Experiment with reading the string table created during one of the previous app runs
        previous_string_table = fileUtil.readStringTable(ctx)
        
        # Run the FBA apps using KBParallel
        tasks = runner.createTasks(params)
        kbparallel_result = runner.runKBParallel(tasks)
        fba_refs = runner.getFBARefs(kbparallel_result)

        # Set of objects created during this app run (will be linked to in the report at the end)
        # To start, this includes a link for each FBA output created during the KBParallel run
        objects_created = [{'ref': fba_refs[i], 'description': f'results of running fba configuration {i}'} for i in range(0, len(fba_refs))]

        # Save the results into a string data table
        # (if successful, this will be another object linked to in the final report)
        tableData = outputUtil.createTableData(tasks)
        string_data_table = fileUtil.writeStringTable(ctx, params, tableData)
        if string_data_table is not None:
          objects_created.append(string_data_table)

        # HTML table displayed to the user in the report at the end
        summary = outputUtil.createSummary(tasks, kbparallel_result)

        # Extra message to help debug (if detailed logs are enabled)
        debug_message = ''
        if params["detailed_logs"] == 1:
          debug_message += '<br />'
          debug_message += f'<p>KBParallel result:</p><pre>{json.dumps(kbparallel_result, indent=2)}</pre>'
          fba_outputs = fileUtil.readFBAOutputs(ctx, fba_refs)
          if fba_outputs is not None:
            debug_message += f'<p>FBA outputs:</p><pre>{json.dumps(fba_outputs, indent=2)}</pre>'
          if previous_string_table is not None:
            debug_message += f'<p>String table (created during previous app run):</p><pre>{json.dumps(previous_string_table, indent=2)}</pre>'

        # Create the output report
        report = KBaseReport(self.callback_url)          
        report_info = report.create(
          {
            'report': {
              'objects_created': objects_created,
              'text_message': f'{summary}{debug_message}'
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

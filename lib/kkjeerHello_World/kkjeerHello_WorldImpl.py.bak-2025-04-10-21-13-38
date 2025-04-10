# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
import json

from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.KBParallelClient import KBParallel

from available_tasks import TASKS

# from biokbase.narrative.appeditor import generate_app_cell
# nms = biokbase.narrative.clients.get('narrative_method_store')
#END_HEADER


class kkjeerHello_World:
    '''
    Module Name:
    kkjeerHello_World

    Module Description:
    A KBase module: kkjeerHello_World
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.2"
    GIT_URL = "https://github.com/kkjeer/kkjeerAppRunner"
    GIT_COMMIT_HASH = "HEAD"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        #END_CONSTRUCTOR
        pass


    def run_kkjeerHello_World(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_kkjeerHello_World
        print('Starting Hello_World run function')

        # ws = biokbase.narrative.clients.get('workspace')
        # obj = ws.get_objects2({'objects' : [{'ref' : '79/16/1'}]})
        # print(f'Got obj: {obj}')

        # a_spec = nms.get_method_spec({'ids': ['kb_ea_utils/fastq_stats'], 'tag': 'release'})[0]
        # print(f'Got a_spec: {a_spec}')

        dropdownItems = list(set([obj["select_app"] for obj in params["param_group"]]))

        parallel_runner = KBParallel(self.callback_url)
        tasks = [TASKS[t] for t in dropdownItems]
        batch_run_params = {
          'tasks': tasks,
          'runner': 'parallel',
          'concurrent_local_tasks': 1,
          'concurrent_njsw_tasks': 2,
          'max_retries': 2
        }
        result = parallel_runner.run_batch(batch_run_params)

        report = KBaseReport(self.callback_url)
        report_info = report.create(
          {
            'report': {
              'objects_created':[
                {
                  'ref': '79/16/1',
                  'description': 'ran parallel runner'
                }
              ],
              'text_message': f'<p>Dropdown items: {dropdownItems}</p><p>All params: {json.dumps(params, indent=2)}</p><p>KBParallel result:</p><pre>{json.dumps(result, indent=2)}</pre>'
            },
            'workspace_name': params['workspace_name']
          }
        )
        output = {
            'report_name': report_info['name'],
            'report_ref': report_info['ref'],
        }
        #END run_kkjeerHello_World

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_kkjeerHello_World return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]

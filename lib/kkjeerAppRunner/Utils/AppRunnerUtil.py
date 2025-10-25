import logging
import os

from installed_clients.KBParallelClient import KBParallel

# This class is responsible for running multiple instance of
# the flux_balance_analysis app, given a set of parameter configurations.
class AppRunnerUtil:
  def __init__(self, config):
    self.config = config
    self.callback_url = os.environ['SDK_CALLBACK_URL']
    self.ws_url = config["workspace-url"]
    self.shared_folder = config['scratch']
    logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                        level=logging.INFO)

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
    logging.info(f'Tasks: {tasks}')
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
  
  # This method returns the set of refs to output objects created by a KBParallel run.
  def getFBARefs(self, kbparallel_result):
    fba_refs = []
    for r in kbparallel_result['results']:
      new_fba_ref = r['final_job_state']['result'][0]['new_fba_ref']
      fba_refs.append(new_fba_ref)
    return fba_refs
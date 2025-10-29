import logging
import os
import uuid

# This class is responsible for constructing objects that will be used in output files and reports.
class OutputUtil:
  def __init__(self, config):
    self.config = config
    self.callback_url = os.environ['SDK_CALLBACK_URL']
    self.ws_url = config["workspace-url"]
    self.shared_folder = config['scratch']
    logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                        level=logging.INFO)
  
  # This method creates a JSON object that contains the parameters and outputs of each FBA run.
  def createOutputJson(self, tasks, kbparallel_result):
    result = {}

    param_names = list(tasks[0]['parameters'].keys())
    param_names = [item for item in param_names if item != "workspace"]

    for i in range(0, len(tasks)):
      key = f'row_{i}'

      t = tasks[i]
      p = t['parameters']

      # Get information from the fba result
      r = kbparallel_result['results'][i]['final_job_state']['result'][0]
      objective = r['objective']
      new_fba_ref = r['new_fba_ref']

      obj = {}
      for param in param_names:
        obj[param] = str(p[param])
      obj['objective_value'] = str(objective)
      obj['result_ref'] = new_fba_ref
    
      result[key] = obj
    return result
    
  # This method creates the data used to populate the StringDataTable file that will be written to the workspace.
  # If the output file format changes, this method should be updated.
  def createTableData(self, output_json):
    rows = list(output_json.keys())
    cols = list(output_json[rows[0]].keys())

    table_data = {
      'row_ids': rows,
      'row_labels': rows,
      'column_ids': cols,
      'column_labels': cols,
      'row_groups_ids': [],
      'column_groups_ids': [],
      'data': []
    }

    for r in rows:
      table_data['data'].append(list(output_json[r].values()))

    logging.info(f'table data: {table_data}')

    return table_data
  
  def createSampleSetData(self, output_json):
    sample_set_data = {
      'samples': [
        {'id': str(uuid.uuid4()), 'name': 'first sample', 'version': 1},
        {'id': str(uuid.uuid4()), 'name': 'second sample', 'version': 2}
      ],
      'description': 'my sample set'
    }
    return sample_set_data
  
  def createAttributeMappingData(self, output_json):
    mapping_data = {
      'instances': {},
      'attributes': [],
      'ontology_mapping_method': 'User curation'
    }
    return mapping_data
  
  # This method creates a stringified HTML table containing the results of the FBA runs.
  # This table can be appended to the app summary that is displayed to the user.
  def createSummary(self, output_json):
    rows = list(output_json.keys())
    cols = list(output_json[rows[0]].keys())

    # Top row: column names
    summary = "<table>"
    summary += "<tr>"
    for h in cols:
      summary += f'<th style="padding: 5px">{h}</th>'
    summary += "</tr>"

    # Add each row to the table
    for i in range(0, len(rows)):
      row = rows[i]

      # Open new row
      summary += "<tr style=\"border-top: 1px solid #505050;\">"

      # Define the style of each column
      bg = "#f4f4f4" if i % 2 == 1 else "transparent"
      style = f'style="padding: 5px; background-color: {bg};"'

      # Add the value for each column
      for col in output_json[row]:
        summary += f'<td {style}">{output_json[row][col]}</td>'

      # Close row
      summary += "</tr>"

    summary += "</table>"
    return summary
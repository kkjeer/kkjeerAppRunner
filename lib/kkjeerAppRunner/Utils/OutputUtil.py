import logging
import os

# This class is responsible for constructing objects that will be used in output files and reports.
class OutputUtil:
  def __init__(self, config):
    self.config = config
    self.callback_url = os.environ['SDK_CALLBACK_URL']
    self.ws_url = config["workspace-url"]
    self.shared_folder = config['scratch']
    logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                        level=logging.INFO)
    
  def createParamNames(self, tasks):
    param_names = list(tasks[0]['parameters'].keys())
    param_names = [item for item in param_names if item != "workspace"]
    return param_names
    
  def createTableHeaders(self, param_names):
    table_headers = param_names + ['objective value', 'result ref']
    return table_headers
  
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
        obj[param] = p[param]
      obj['objective_value'] = objective
      obj['result_ref'] = new_fba_ref
    
      result[key] = obj
    return result
    
  # This method creates the data used to populate the StringDataTable file that will be written to the workspace.
  # If the output file format changes, this method should be updated.
  def createTableData(self, tasks, kbparallel_result):
    tableData = {
      'row_ids': [],
      'column_ids': [],
      'row_labels': [],
      'column_labels': [],
      'row_groups_ids': [],
      'column_groups_ids': [],
      'data': []
    }

    param_names = self.createParamNames(tasks)
    table_headers = self.createTableHeaders(param_names)
    tableData['column_ids'] = table_headers
    tableData['column_labels'] = table_headers

    for i in range(0, len(tasks)):
      tableData['row_ids'].append(f'row{i}')
      tableData['row_labels'].append(f'row {i}')

      t = tasks[i]
      p = t['parameters']

      # Get information from the fba result
      r = kbparallel_result['results'][i]['final_job_state']['result'][0]
      objective = r['objective']
      new_fba_ref = r['new_fba_ref']

      # The data for this row in the table is each parameter value in the task
      # plus the output values from the fba result
      data = [str(p[name]) for name in param_names]
      data.append(str(objective))
      data.append(new_fba_ref)

      tableData['data'].append(data)

    return tableData
  
  def createSummary(self, tasks, kbparallel_result):
    param_names = self.createParamNames(tasks)
    table_headers = self.createTableHeaders(param_names)

    # Top row: name of each parameter plus the values from the fba result
    summary = "<table>"
    summary += "<tr>"
    for h in table_headers:
      summary += f'<th style="padding: 5px">{h}</th>'
    summary += "</tr>"

    for i in range(0, len(tasks)):
      # Get the parameters passed to the task
      t = tasks[i]
      p = t['parameters']

      # Get information from the fba result
      r = kbparallel_result['results'][i]['final_job_state']['result'][0]
      objective = r['objective']
      new_fba_ref = r['new_fba_ref']

      # Open new row
      summary += "<tr style=\"border-top: 1px solid #505050;\">"

      # Define the style of each column
      bg = "#f4f4f4" if i % 2 == 1 else "transparent"
      style = f'style="padding: 5px; background-color: {bg};"'

      # Add each parameter the user configured via the UI as a column in the table
      for name in param_names:
        summary += f'<td {style}">{p[name]}</td>'
      
      # Add the last two columns (from the fba result)
      summary += f'<td {style}>{objective}</td>'
      summary += f'<td {style}>{new_fba_ref}</td>'

      # Close row
      summary += "</tr>"

    summary += "</table>"
    return summary
TASKS = {
  'kb_Bowtie2': {
    'module_name': 'kb_Bowtie2',
    'function_name': 'align_reads_to_assembly_app',
    'version': 'dev',
    'parameters': {
      'alignment_type': 'end-to-end',
      'assembly_or_genome_ref': '75203/10/1',
      'condition_label': 'unknown',
      'input_ref': '75203/9/2',
      'maxins': 500,
      'minins': 0,
      'np': 1,
      'orientation': None,
      'output_alignment_suffix': '_alignment',
      'output_obj_name_suffix': '_alignment_set',
      'output_workspace': 'kkjeer:narrative_1740693446851',
      'preset_options': None,
      'quality_score': 'phred33',
      'trim3': 0,
      'trim5': 0
    }
  },
  'fba_tools': {
    'module_name': 'fba_tools',
    'function_name': 'run_flux_balance_analysis',
    'version': 'release',
    'parameters': {
      'fbamodel_id': '75203/14/1',
      'target_reaction': '4HBTE_c0',
      'fba_output_id': 'kbparallel-fba-output',
      'workspace': 'kkjeer:narrative_1740693446851',
    }
  }
}
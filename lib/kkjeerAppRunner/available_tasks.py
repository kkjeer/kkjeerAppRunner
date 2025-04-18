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
      'workspace': 'kkjeer:narrative_1740693446851'
    }
  },
  'CGViewAdvanced': {
    'module_name': 'CGViewAdvanced',
    'function_name': 'run_CGViewAdvanced',
    'version': 'release',
    'parameters': {
      "input_file": "75203/10/1",
      "linear": 1,
      "gc_content": 1,
      "gc_skew": 1,
      "at_content": 0,
      "at_skew": 0,
      "average": 1,
      "scale": 1,
      "orfs": 0,
      "combined_orfs": 0,
      "orf_size": 100,
      "tick_density": 0.5,
      "details": 1,
      "legend": 1,
      "condensed": 0,
      "feature_labels": 0,
      "orf_labels": 0,
      "show_sequence_features": 1,
      "workspace_name": 'kkjeer:narrative_1740693446851'
    }
  },
  'Weka': {
    'module_name': 'Weka',
    'function_name': 'decision_tree',
    'version': 'release',
    'parameters': {
      "phenotype_ref": "75203/54/1",
      "confidenceFactor": "0.25",
      "minNumObj": "2",
      "numFolds": "3",
      "seed": "1",
      "unpruned": 0,
      "class_values": "0,1",
      "class_labels": "NO_GROWTH,GROWTH"
    }
  }
}
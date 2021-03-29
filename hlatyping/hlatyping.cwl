#!/usr/bin/env cwl-runner

# (Re)generated by BlueBee Platform

$namespaces:
  bb: http://bluebee.com/cwl/
  ilmn-tes: http://platform.illumina.com/rdf/iap/
cwlVersion: cwl:v1.0
class: CommandLineTool
bb:toolVersion: '1'
requirements:
- class: InlineJavascriptRequirement
- class: InitialWorkDirRequirement
  listing:
  - |
    ${
        var fastq_files_array = inputs.FASTQ_files;
        var bam_file_array = inputs.BAM_file;
        var output_array = [];

    if ( fastq_files_array != null ){
      for (var i=0; i<fastq_files_array.length; i++){
        output_array.push(fastq_files_array[i])
      }
    }

    if ( bam_file_array != null ){
          output_array.push(inputs.BAM_file)
    }
     return output_array
    }
label: hlatyping_nf_tool
doc: hlatyping_nf_tool based off of https://github.com/nf-core/hlatyping
inputs:
  FASTQ_files:
    type:
      type: array
      items: File
    inputBinding:
      prefix: --fastq_files
  BAM_file:
    type:
    - File
    - 'null'
    inputBinding:
      prefix: --bam
  fastq suffix:
    type:
    - string
    - 'null'
    inputBinding:
      prefix: --fastq_pattern
outputs:
  Output Dir:
    type:
    - Directory
    - 'null'
  log files:
    type:
    - type: array
      items: File
    - 'null'
    outputBinding:
      glob:
      - '*log'
  HLA result:
    type: File
    outputBinding:
      glob:
      - '*tsv'
  html reports:
    type:
    - type: array
      items: File
    - 'null'
    outputBinding:
      glob:
      - '*html'
  'coverage plots ':
    type:
    - File
    - 'null'
    outputBinding:
      glob:
      - '*pdf'
arguments:
- position: 2
  prefix: --output_directory
  valueFrom: $(runtime.outdir)
baseCommand:
- /opt/conda/envs/nf-core-hlatyping-1.2.0/bin/python
- /opt/tool_wrapper_nf.py
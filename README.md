- Used Nextflow pipeline [hlatyping](https://github.com/nf-core/hlatyping)
- [Docker image](https://github.com/keng404/nextflow_test/blob/master/Dockerfile) you base your nextflow-based tool would need nextflow to run the pipeline and have the binaries of interest installed. Many nextflow pipelines have a conda profile to install all binaries of interest with a single line of code.
- Main thing is to check out each process defined in nextflow scripts ( e.g. usually files with '.nf' extension) and make sure the parameter **publishDir** is defined. This will allow ICA to collect the results of any process of interest. For Example:
```bash
process < name > {
    publishDir "", mode: copy
   [ directives ]

   input:
    < process inputs >

   output:
    < process outputs >

   [script|shell|exec]:
   < user script to be executed >

}
```
- You will need to run **nextflow clean -f** to remove cache and work directories of a pipeline run. There are symlinked files which makes the folder/file-syncing of ICA to fail.
- See a simple wrapper script [here](https://github.com/keng404/nextflow_test/blob/master/tool_wrapper_nf.py). Nextflow is invoked like so:
```
nextflow run /opt/hlatyping/main.nf -profile conda--input ${INPUT_DIR}/${STRING_TO_GLOB_FASTQs} --output_dir ${OUTPUT_PATH} -work-dir ${WORKDIR_PATH}
```
Notes: ${WORKDIR_PATH} and ${OUTPUT_PATH} should be different directories to prevent causing ICA to copy intermediate files and cause UI issues. The CWL of the tool is provided [here](https://github.com/keng404/nextflow_test/blob/master/hlatyping/hlatyping.cwl).

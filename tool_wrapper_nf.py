#!/usr/bin/python3
import argparse
import os
import json
import shlex
import subprocess

def execute_command(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process.communicate()

def log_command(cmd, log_object):
	out,err = execute_command(cmd) 
	log_object.write(out.decode('utf8'))
	log_object.write(err.decode('utf8'))


def run_nf(inputs,bamfile,output_dir,additional_args):
	# create working directory that is different from output directory . 
	# This will prevent ICA from copying intermediate files. Especially since in this pipeline, we are choosing conda installations of tools, this will result in > 20k files
	work_dir = '/scratch'
	os.makedirs(work_dir, exist_ok=True)
	if inputs is not None:
		full_cmd = ['/opt/conda/bin/nextflow' ,'run' ,'/opt/hlatyping/main.nf','-profile','conda','--input',inputs,'--outdir',output_dir,'-work-dir',work_dir]
	else:
		full_cmd = ['/opt/conda/bin/nextflow' ,'run' ,'/opt/hlatyping/main.nf','-profile','conda','--bam', bamfile,'--outdir',output_dir,'-work-dir',work_dir]
	if additional_args:
		full_cmd.append(additional_args)
	full_cmd_str = " ".join(full_cmd)
	full_cmd = shlex.split(full_cmd_str)
	print(full_cmd)
	print("Running:\t" + full_cmd_str)
	out,err = execute_command(full_cmd)
	run_log = open("run.log","w")
	run_log.writelines("%s\n" % full_cmd_str)
	run_log.write(err.decode("utf8"))
	run_log.write(out.decode("utf8"))
	####### Clean up cache and working directories
	cleanup_cmd_str = '/opt/conda/bin/nextflow clean -f'
	cleanup_cmd = shlex.split(cleanup_cmd_str)
	print("Running:\t" + cleanup_cmd_str)
	log_command(cleanup_cmd,run_log)
	## explicity remove cache and working directories
	cleanup_cmd1 = shlex.split('rm -rf '  + work_dir)
	print("Running:\t" + ' '.join(cleanup_cmd1))
	log_command(cleanup_cmd1,run_log)
	## explicity remove conda installation to avoid ICA from pulling these files back after a pipeline run
	cleanup_cmd2 = shlex.split('rm -rf ' + work_dir +  '/.conda')
	print("Running:\t" + ' '.join(cleanup_cmd2))
	log_command(cleanup_cmd2,run_log)
	cleanup_cmd2 = shlex.split('rm -rf ' + '.conda')
	print("Running:\t" + ' '.join(cleanup_cmd2))
	log_command(cleanup_cmd2,run_log)
	## explicity remove cache and working directories
	cleanup_cmd3 = shlex.split('rm -rf ' + work_dir + "/" + '.nextflow')
	print("Running:\t" + ' '.join(cleanup_cmd3))
	log_command(cleanup_cmd3,run_log)
	cleanup_cmd3 = shlex.split('rm -rf ' + '.nextflow')
	print("Running:\t" + ' '.join(cleanup_cmd3))
	log_command(cleanup_cmd3,run_log)
	run_log.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fastq_files',nargs = '*', default = [],type = str, help="FASTQ files to HLA type")
    parser.add_argument('--bam',type = str,help="input BAM file")
    parser.add_argument('--fastq_pattern', default='*_R{1,2}.fastq.gz',type = str, help="pattern to obtain FASTQ files of interest")
    parser.add_argument('--output_directory',type = str, help = "output directory that will contain results")
    args, extras = parser.parse_known_args()
    inputs_str = None
    if args.bam is None:
    	input_dir = list(set([os.path.dirname(x) for x in args.fastq_files]))[0]
    	inputs_str = '\'' + input_dir + "/" + args.fastq_pattern + '\'' 
    	print("Grabbing fastqs from this pattern:\t" + inputs_str + "\n")
    run_nf(inputs_str,args.bam,args.output_directory,extras)


if __name__ == '__main__':
    main()

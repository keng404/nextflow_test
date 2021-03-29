FROM nfcore/base:1.10.2
LABEL authors="Christopher Mohr, Alexander Peltzer, Sven Fillinger, Ken Eng <keng@illumina.com>" \
      description="Docker image containing all software requirements for the nf-core/hlatyping pipeline"
# Install the conda environment
COPY environment.yml /opt
RUN conda env create --quiet -f /opt/environment.yml && conda clean -a

# Add conda installation dir to PATH (instead of doing 'conda activate')
ENV PATH /opt/conda/envs/nf-core-hlatyping-1.2.0/bin:$PATH

# Dump the details of the installed packages to a file for posterity
RUN conda env export --name nf-core-hlatyping-1.2.0 > nf-core-hlatyping-1.2.0.yml
RUN conda install -c bioconda nextflow
# Instruct R processes to use these empty files instead of clashing with a local version
RUN touch .Rprofile
RUN touch .Renviron

## copy nextflow pipeline files into container
COPY hlatyping  /opt/hlatyping
COPY tool_wrapper_nf.py /opt
## add virtual environment by default into container
RUN echo "source activate nf-core-hlatyping-1.2.0" > ~/.bashrc
# NosZRef: an integrated database and pipeline for rapid and accurate profiling of *nosZ* genes
Version：v1.0.0

Update：2026/03/28

## Background
To accurately analyze microbially driven nitrous oxide reduction, current databases and bioinformatics tools face critical limitations. Existing nitrogen-cycle databases, such as NCycDB, lack standardized analytical thresholds, leading to high false-positive rates, and contain ambiguous taxonomic classifications while applying inappropriate uniform clustering cutoffs to functionally diverse genes such as *nosZ*. Furthermore, although metagenomics overcomes the primer bias inherent in amplicon sequencing, available analysis pipelines remain fragmented, with current tools either designed for specific tasks or, like web-based platforms, lacking the flexibility required for large-scale or customized analyses. Therefore, a comprehensive solution is urgently needed, necessitating the development of a rigorously curated database with gene-specific thresholds for similarity and taxonomy, coupled with an integrated, user-friendly open-source pipeline to enable precise, high-throughput profiling of *nosZ*-harboring communities. To address this need, we developed the NosZRef pipeline.

## Pipeline manual and file description

Files description:

- README.md     # Introduction and install
- database      # Directory for `DIAMOND` functional gene index and reference database files
- software      # Directory for analysis software used in the pipeline
- sub           # Directory for all Python and R scripts used in the pipeline
- `raw_main.py`                   # Main script file
- Example_data   # Example dataset

## What can we do?

- Comprehensive analysis and visualization of *nosZ*-I, *nosZ*-II, and *nosZ*-III genes;
- From raw sequencing data to functional gene abundance tables and microbial community profiles;
- Accurate identification of *nosZ* genes using gene-specific thresholds to minimize false positives;

![Figure 1](https://raw.githubusercontent.com/ZhangBaoshan668/Figure/main/NosZfig1.jpg)

**Figure 1. NosZRef workflow. (A) Flowchart of major steps for *nosZ* database construction. (B) Schematic of the data analysis workflow for *nosZ* genes. (C) Schematic overview of statistical and visual analyses in NosZRef command-line mode.**

## Main Features
+ Preprocessing and normalization of nitrogen cycling functional gene sequencing data
+ Functional gene abundance visualization
+ Taxonomic abundance visualization
+ Alpha diversity
+ Beta diversity
+ Differential abundance test
+ Network analysis

![Figure 2](https://raw.githubusercontent.com/ZhangBaoshan668/Figure/main/fig2.jpg)

**Figure 2. Representative publication-ready visualizations.**

## Install

### Install Conda and R package

    # Create a new directory named “miniconda3” in your home directory.
    mkdir -p ~/miniconda3
    
    # Download the Linux Miniconda installation script for your chosen chip architecture and save the script as “miniconda.sh” in the miniconda3 directory.
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
    
    # Run the “miniconda.sh” installation script in silent mode using bash.
    bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3

    # Remove the “miniconda.sh” installation script file after installation is complete.
    rm ~/miniconda3/miniconda.sh

    # After installing, close and reopen your terminal application or refresh it by running the following command:
    source ~/miniconda3/bin/activate

    # Then, initialize conda on all available shells by running the following command:
    conda init --all

    # Add frequently used channels
    conda config --add channels bioconda
    conda config --add channels conda-forge
    conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free
    conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
    conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
    conda config --set show_channel_urls yes

    # Create and activate NosZRef environment
    conda create -n NosZRef
    conda activate NosZRef

    # Conda install R
    conda install r-base=4.4.1

    # Install R package
    conda install r-BiocManager
    conda install r-ggplot2
    conda install r-devtools
    conda install r-vegan
    conda install r-igraph
    conda install r-dplyr
    conda install r-Hmisc
    conda install r-optparse
    conda install r-purrr
    conda install r-ggpubr
    conda install r-ggprism

    # Install amplicon package
    ## Enter R environment
    R
    library(devtools)
    install_github("microbiota/amplicon")
    ## Exit R environment
    q()

### Install NosZRef

    # Create a new directory named “NosZRef” in your home directory. 
    mkdir NosZRef
    cd NosZRef

    # Downdoald NosZRef pipeline from github.
    git clone https://github.com/ZhangBaoshan668/NosZRef.git

**Note: `fatal: unable to access` can retry.**

## Introduction to NosZRef pipeline parameters

    # Parameter explanation
    cd NosZRef
    
    python3 raw_main.py -h
    usage: raw_main.py [-h] -i INPUT -l LIS -o OUTDIR -m GROUP [-t THREADS] [-v]
    nosZ gene analysis pipeline - Simultaneous analysis of nosZI, nosZII, and nosZIII branches
    options:
      -h, --help            show this help message and exit
      -i INPUT, --input INPUT
                        Input directory (containing raw sequencing data)
      -l LIS, --lis LIS     Sample list file (format: original_filename sample_name)
      -o OUTDIR, --outdir OUTDIR
                        Output directory
      -m GROUP, --group GROUP
                        Group list file
      -t THREADS, --threads THREADS
                        Number of parallel threads (default: 20)
      -v, --version         Display version and author information

    Examples:
      python3 raw_main.py -i ./ -l sample.list -o ./ -m group.list

**Note: The parameters -i, -l, -m and -o are essential for the execution of the main script. The parameters -t is set as default values in the script, and their settings can also be adjusted according to specific needs.**

## Quick Start

    # Create work directory
    mkdir example
    cd example

    # Enter Conda environment
    conda activate NosZRef

    # Create the "raw_data" folder in the working directory and the folder must be named "raw_data".
    # In the "raw_data" folder, only the single-end sequencing data of high-throughput sequencing should be stored, such as "_1.fastq.gz" or "_1.fq.gz".
    mkdir raw_data

    # Create "list.txt", "gene.txt", and "metadata.txt" file
    touch list.txt metadata.txt
  
- **The `list.txt` file contains two columns of information. The first column represents the original sample number, and the second column represents the renamed sample number. The two columns are separated by a `tab`.**

![Figure 3](https://raw.githubusercontent.com/ZhangBaoshan668/Figure/main/fig3.jpg)

- **The `metadata.txt` file must have a header row, with the columns labeled as `SampleID` and `Group`. The content of the header cannot be changed and it should contain two columns of information. The first column contains the renamed sample number, and the second column contains the sample grouping information. The two columns are separated by a `tab`.**

![Figure 4](https://raw.githubusercontent.com/ZhangBaoshan668/Figure/main/fig4.jpg)

**The `example` folder should contain the `raw_data` folder, `list.txt` and `metadata.txt`. Then, by running the main script file `raw_main.py` in the `example` folder, the analysis can be started.**

    # Running with default parameters
    
    python3 /your_path/raw_main.py -i ./ -l list.txt -m metadata.txt -o ./

**Note: The main script must be run from the path of the `example` folder.**

## FAQ & Contributing

Please report errors and questions on Github [Issues](https://github.com/ZhangBaoshan668/NosZRef/issues).

Any contribution via [Pull requests](https://github.com/ZhangBaoshan668/NosZRef/pulls) will be appreciated.
















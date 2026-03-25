#!/usr/bin/python3

import argparse
import os
import glob
import re
import threading
import shutil

# Define version number and author information
VERSION = "2.0.0"
AUTHOR = "MEG"

# Define nosZ gene information
NOSZ_GENES = {
        'nosZI': {
        'similarity': 64,      # Similarity threshold (%)
        'query_cover': 75,     # Query coverage threshold (%)
        'evalue': 1e-5,        # E-value threshold
        'database': 'nosZI.dmnd',
        'cluster': 0.86,
        'gene_length': 1920
    },
    'nosZII': {
        'similarity': 61,
        'query_cover': 75,
        'evalue': 1e-5,
        'database': 'nosZII.dmnd',
        'cluster': 0.85,
        'gene_length': 2046
    },
    'nosZIII': {
        'similarity': 77,
        'query_cover': 75,
        'evalue': 1e-5,
        'database': 'nosZIII.dmnd',
        'cluster': 0.86,
        'gene_length': 939
    }
}

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='nosZ gene analysis pipeline - Simultaneous analysis of nosZI, nosZII, and nosZIII branches',
    epilog="""
Examples:
  python3 nosZ_pipeline.py -i raw_data -l sample.list -o output -m group.list -t 20
    """
)
parser.add_argument('-i', '--input', required=True, type=str, help='Input directory (containing raw sequencing data)')
parser.add_argument('-l', '--lis', required=True, type=str, help='Sample list file (format: original_filename sample_name)')
parser.add_argument('-o', '--outdir', required=True, type=str, help='Output directory')
parser.add_argument('-m', '--group', required=True, type=str, help='Group list file')
parser.add_argument('-t', '--threads', type=int, default=20, help='Number of parallel threads (default: 20)')
parser.add_argument('-v', '--version', action='store_true', help='Display version and author information')

args = parser.parse_args()

if args.version:
    print(f"Version: {VERSION}")
    print(f"Author: {AUTHOR}")
    print("\nnosZ gene branch parameters:")
    for nosz_type, config in NOSZ_GENES.items():
        print(f"  {nosz_type}: Similarity threshold = {config['similarity']}%, Coverage = {config['query_cover']}%")
    exit(0)

# Get parameters
input_dir = os.path.abspath(args.input)
sample_list = args.lis
outdir = args.outdir
threads = args.threads
group_list = args.group

# Check input directory
if not os.path.exists(input_dir):
    print(f"Error: Input directory does not exist: {input_dir}")
    exit(1)

# Set output directory
out_path = os.path.abspath(outdir)
if not os.path.exists(out_path):
    os.mkdir(out_path)

# Get script directory
script_dir = os.path.dirname(os.path.realpath(__file__))
sub_dir = os.path.join(script_dir, "sub")
db_dir = os.path.join(script_dir, "database")
software_dir = os.path.join(script_dir, "software")

# Read sample list, create mapping: original filename -> sample name
rename_dict = {}
sample_names = []
if os.path.exists(sample_list):
    with open(sample_list, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith('#'):
                parts = line.strip().split()
                if len(parts) >= 2:
                    original, new = parts[0], parts[1]
                    rename_dict[original] = new
                    sample_names.append(new)
                else:
                    rename_dict[parts[0]] = parts[0]
                    sample_names.append(parts[0])
else:
    print(f"Error: Sample list file does not exist: {sample_list}")
    exit(1)

# Get full paths of all sequencing files in input directory
print("Scanning input directory...")
all_input_files = {}
for root, dirs, files in os.walk(input_dir):
    for file in files:
        if file.endswith(('.gz', '.fq', '.fastq', '.fq.gz', '.fastq.gz')):
            full_path = os.path.join(root, file)
            all_input_files[file] = full_path

print(f"Found {len(all_input_files)} sequencing files in input directory")

# Create mapping: original filename -> file path
file_mapping = {}
for original, new in rename_dict.items():
    found_path = None
    
    # Multiple matching strategies
    for filename, filepath in all_input_files.items():
        # Strategy 1: Exact match
        if filename == original or filename == original + '.gz':
            found_path = filepath
            break
        # Strategy 2: Starts with original filename
        if filename.startswith(original):
            found_path = filepath
            break
        # Strategy 3: Original filename contained in filename
        if original in filename:
            found_path = filepath
            break
        # Strategy 4: Match after removing extensions
        base = re.sub(r'\.(fq|fastq|gz)$', '', filename)
        base = re.sub(r'\.gz$', '', base)
        if base == original or base.startswith(original):
            found_path = filepath
            break
    
    if found_path:
        file_mapping[new] = found_path
        print(f"  ✓ Sample '{new}' corresponds to file: {os.path.basename(found_path)}")
    else:
        print(f"  ⚠ Warning: No file found matching '{original}', skipping this sample")

if not file_mapping:
    print("Error: No valid sample files found")
    exit(1)

# Create output directory structure
shell_path = os.path.join(out_path, "shell")
if not os.path.exists(shell_path):
    os.mkdir(shell_path)

# Create directory for each sample
for samp in file_mapping.keys():
    samp_path = os.path.join(out_path, samp)
    if not os.path.exists(samp_path):
        os.mkdir(samp_path)

# Generate processing script for each sample
print("\nGenerating sample processing scripts...")
valid_samples = []
for samp, input_file in file_mapping.items():
    samp_path = os.path.join(out_path, samp)
    valid_samples.append(samp)
    
    print(f"  ✓ Generating script: {samp}.sh (Input file: {os.path.basename(input_file)})")
    
    with open(os.path.join(shell_path, samp+".sh"), 'w') as sh_file:
        sh_file.write(f'echo "=========================================="\n')
        sh_file.write(f'echo "Processing sample: {samp}"\n')
        sh_file.write(f'echo "Input file: {input_file}"\n')
        sh_file.write(f'echo "=========================================="\n\n')
        
        # Quality control (use original file path directly, no copying)
        sh_file.write(f'echo "Step 1: Quality control"\n')
        sh_file.write(f'{software_dir}/fastp -i {input_file} -o {samp_path}/{samp}.clean.fq.gz -w 16 -j {samp_path}/{samp}.json\n')
        sh_file.write(f'echo -n "{samp}" | paste - - <(jq \'.summary.after_filtering.total_reads\' {samp_path}/{samp}.json) | awk \'{{print $1 "\t" $2}}\' > {samp_path}/{samp}_total_reads.txt\n\n')
        
        # Convert to fasta
        sh_file.write(f'echo "Step 2: Convert to FASTA format"\n')
        sh_file.write(f'{software_dir}/seqtk seq -a {samp_path}/{samp}.clean.fq.gz > {samp_path}/{samp}.fa\n')
        sh_file.write(f'awk \'BEGIN{{FS=""; OFS=""; id=1}} /^>/ {{print ">{samp}_"id++; next}} {{print}}\' {samp_path}/{samp}.fa > {samp_path}/{samp}.rename.fa\n\n')
        
        # Process each nosZ branch
        for nosz_type, nosz_config in NOSZ_GENES.items():
            similarity = nosz_config['similarity']
            query_cover = nosz_config['query_cover']
            evalue = nosz_config['evalue']
            gene_length = nosz_config['gene_length']
            db_file = os.path.join(db_dir, nosz_config['database'])
            
            sh_file.write(f'echo "=========================================="\n')
            sh_file.write(f'echo "Processing {nosz_type} (Similarity: {similarity}%, Coverage: {query_cover}%)"\n')
            sh_file.write(f'echo "=========================================="\n')
            
            # DIAMOND blastx
            sh_file.write(f'{software_dir}/diamond blastx -d {db_file} -q {samp_path}/{samp}.rename.fa -o {samp_path}/{nosz_type}_{samp}.txt -e {evalue} --id {similarity} --query-cover {query_cover} -f 6 -p 140 -k 1\n')
            
            # Count sequences
            sh_file.write(f'paste -d "\t" <(echo -n "{samp}") <(cat {samp_path}/{nosz_type}_{samp}.txt | cut -f1 | sort | uniq | wc -l) > {samp_path}/{nosz_type}_{samp}.result.txt\n')
            
            # Extract unique sequence IDs
            sh_file.write(f'cat {samp_path}/{nosz_type}_{samp}.txt | cut -f1 | sort | uniq > {samp_path}/{nosz_type}_{samp}.id\n')
            
            # Extract target sequences
            sh_file.write(f'{software_dir}/seqtk subseq {samp_path}/{samp}.rename.fa {samp_path}/{nosz_type}_{samp}.id > {samp_path}/{nosz_type}_{samp}.target.fa\n')            
            
            # BLASTX species annotation
            sh_file.write(f'{software_dir}/blastx -db {db_dir}/{nosz_type} -query {samp_path}/{nosz_type}_{samp}.target.fa -out {samp_path}/{nosz_type}_{samp}.tax_result.txt -max_target_seqs 1 -outfmt "6 qseqid qlen sseqid sgi slen pident length mismatch gapopen qstart qend sstart send evalue bitscore staxid ssciname" -num_threads 50 -evalue 1e-3\n')
            
            # Species classification statistics
            sh_file.write(f'python3 {sub_dir}/tax_statistics.py {nosz_type} {samp} {samp_path}/{nosz_type}_{samp}.tax_result.txt\n')
            
            # Calculate CPM
            sh_file.write(f'# Calculate {nosz_type} CPM/RPKM values\n')
            sh_file.write(f'TOTAL_READS=$(cat {samp_path}/{samp}_total_reads.txt | cut -f2)\n')
            sh_file.write(f'echo "Total reads: $TOTAL_READS"\n')
            sh_file.write(f'python3 {sub_dir}/calculate_cpm.py {samp_path} {samp} $TOTAL_READS {nosz_type} {gene_length}\n\n')
        
        # Clean up temporary files
        sh_file.write(f'echo "Cleaning up temporary files"\n')
        sh_file.write(f'rm -rf {samp_path}/{samp}.clean.fq.gz\n')
        sh_file.write(f'rm -rf {samp_path}/{samp}.fa\n')
        sh_file.write(f'rm -rf {samp_path}/{samp}.rename.fa\n')
        sh_file.write(f'echo "Sample {samp} processing completed"\n')

# Generate parallel execution script for all samples
with open(os.path.join(shell_path, "all.sample.sh"), 'w') as all_sh:
    all_sh.write('#!/bin/bash\n')
    all_sh.write('echo "Starting parallel processing of all samples"\n\n')
    for samp in valid_samples:
        all_sh.write(f'sh {shell_path}/{samp}.sh\n')

# Execute all sample processing
print("\nExecuting sample processing...")
os.system(f'python3 {sub_dir}/ParallelShellExecutor.py {shell_path}/all.sample.sh {threads}')

# Subsequent steps remain...
print("\nExecuting overlapping sequence allocation (EM algorithm)...")
os.system(f'python3 {sub_dir}/allocate_overlap.py {out_path}')

# Recalculate RPKM
print("\nRecalculating RPKM...")
for samp in valid_samples:
    samp_path = os.path.join(out_path, samp)
    for nosz_type, nosz_config in NOSZ_GENES.items():
        gene_length = nosz_config['gene_length']
        result_file = os.path.join(samp_path, f"{nosz_type}_{samp}.result.txt")
        if os.path.exists(result_file):
            os.system(f'python3 {sub_dir}/calculate_rpkm.py {samp_path}/{samp}_total_reads.txt {result_file} {gene_length} {samp_path} {nosz_type}')

# Generate merge script
with open(os.path.join(shell_path, "merge.sh"), 'w') as sh_merge:
    sh_merge.write('#!/bin/bash\n')
    sh_merge.write('echo "Starting to merge all sample results"\n\n')
    for nosz_type in NOSZ_GENES.keys():
        sh_merge.write(f'echo "Merging {nosz_type} results"\n')
        sh_merge.write(f'mkdir -p {out_path}/merge/{nosz_type}\n')
        sh_merge.write(f'python3 {sub_dir}/merge.py {out_path} {nosz_type}\n')
    sh_merge.write('echo "Merge completed"\n')

os.system(f'sh {shell_path}/merge.sh')

# Generate feature analysis script
with open(os.path.join(shell_path, "feature.sh"), 'w') as otutab:
    otutab.write('#!/bin/bash\n')
    otutab.write('echo "Starting feature analysis (OTU clustering)"\n\n')
    for nosz_type in NOSZ_GENES.keys():
        cluster = NOSZ_GENES[nosz_type]['cluster']
        otutab.write(f'echo "Processing {nosz_type} OTU clustering"\n')
        otutab.write(f'sed -i "s/_[0-9][0-9]*$//" {out_path}/merge/{nosz_type}/{nosz_type}_merged_target.fa 2>/dev/null || true\n')
        otutab.write(f'{software_dir}/usearch -fastx_uniques {out_path}/merge/{nosz_type}/{nosz_type}_merged_target.fa -fastaout {out_path}/merge/{nosz_type}/{nosz_type}_uniques.fa -sizeout -relabel OTU_ -minuniquesize 2\n')
        otutab.write(f'{software_dir}/usearch -cluster_fast {out_path}/merge/{nosz_type}/{nosz_type}_uniques.fa -centroids {out_path}/merge/{nosz_type}/{nosz_type}_otus.fa -uc {out_path}/merge/{nosz_type}/{nosz_type}_clusters.uc -id {cluster} -minsize 2\n')
        otutab.write(f'{software_dir}/vsearch --usearch_global {out_path}/merge/{nosz_type}/{nosz_type}_merged_target.fa --db {out_path}/merge/{nosz_type}/{nosz_type}_otus.fa --id {cluster} --threads 140 --otutabout {out_path}/merge/{nosz_type}/{nosz_type}_otutab.txt\n\n')
    otutab.write('echo "Feature analysis completed"\n')

os.system(f'sh {shell_path}/feature.sh')

# Generate diversity analysis script
with open(os.path.join(shell_path, "diversity.sh"), 'w') as diversity:
    diversity.write('#!/bin/bash\n')
    diversity.write('echo "Starting diversity analysis"\n\n')
    for nosz_type in NOSZ_GENES.keys():
        diversity.write(f'echo "Processing {nosz_type} diversity analysis"\n')
        diversity.write(f'mkdir -p {out_path}/merge/{nosz_type}/alpha {out_path}/merge/{nosz_type}/beta {out_path}/merge/{nosz_type}/network {out_path}/merge/{nosz_type}/taxonomy\n')
        diversity.write(f'{software_dir}/Rscript {sub_dir}/otutab_rare.R --input {out_path}/merge/{nosz_type}/{nosz_type}_otutab.txt --normalize {out_path}/merge/{nosz_type}/alpha/{nosz_type}_otutab_rare.txt --output {out_path}/merge/{nosz_type}/alpha/{nosz_type}_alpha_div.txt\n')
        diversity.write(f'{software_dir}/usearch -otutab_stats {out_path}/merge/{nosz_type}/alpha/{nosz_type}_otutab_rare.txt -output {out_path}/merge/{nosz_type}/alpha/{nosz_type}_otutab_rare.stat\n')
        diversity.write(f'{software_dir}/usearch -alpha_div_rare {out_path}/merge/{nosz_type}/alpha/{nosz_type}_otutab_rare.txt -output {out_path}/merge/{nosz_type}/alpha/{nosz_type}_alpha_rare.txt -method without_replacement\n')
        diversity.write(f'sed -i "s/-/\\t0.0/g" {out_path}/merge/{nosz_type}/alpha/{nosz_type}_alpha_rare.txt\n')
        diversity.write(f'{software_dir}/usearch -beta_div {out_path}/merge/{nosz_type}/alpha/{nosz_type}_otutab_rare.txt -filename_prefix {out_path}/merge/{nosz_type}/beta/\n')
        diversity.write(f'{software_dir}/usearch -otutab_counts2freqs {out_path}/merge/{nosz_type}/alpha/{nosz_type}_otutab_rare.txt -output {out_path}/merge/{nosz_type}/{nosz_type}_otutab_freqs.txt\n\n')
    diversity.write('echo "Diversity analysis completed"\n')

os.system(f'sh {shell_path}/diversity.sh')

# Generate plotting script
with open(os.path.join(shell_path, "plot.sh"), 'w') as plot:
    plot.write('#!/bin/bash\n')
    plot.write('echo "Starting plotting analysis"\n\n')
    for nosz_type in NOSZ_GENES.keys():
        plot.write(f'echo "Plotting {nosz_type} charts"\n')
        plot.write(f'{software_dir}/Rscript {sub_dir}/alpha_rare_curve.R --input {out_path}/merge/{nosz_type}/alpha/{nosz_type}_alpha_rare.txt --design {group_list} --group Group --output {out_path}/merge/{nosz_type}/alpha/ --width 89 --height 59\n')
        
        for index in ['richness', 'chao1', 'shannon', 'simpson', 'invsimpson', 'ACE']:
            plot.write(f'{software_dir}/Rscript {sub_dir}/alpha_boxplot.R --alpha_index {index} --input {out_path}/merge/{nosz_type}/alpha/{nosz_type}_alpha_div.txt --design {group_list} --group Group --output {out_path}/merge/{nosz_type}/alpha/ --width 89 --height 59\n')
        
        plot.write(f'{software_dir}/Rscript {sub_dir}/beta_pcoa.R --input {out_path}/merge/{nosz_type}/beta/bray_curtis.txt --design {group_list} --group Group --output {out_path}/merge/{nosz_type}/beta/{nosz_type}_bray_curtis.pcoa.pdf --width 89 --height 59 --label FALSE\n')
        
        # Species stack plots
        for level in ['phylum', 'class', 'order', 'family', 'genus', 'species']:
            plot.write(f'if [ -f {out_path}/merge/{nosz_type}/{nosz_type}_merged_{level}_rpkm.csv ]; then\n')
            plot.write(f'  {software_dir}/Rscript {sub_dir}/tax_stackplot.R --input {out_path}/merge/{nosz_type}/{nosz_type}_merged_{level}_rpkm.csv --design {group_list} --group Group --color Paired --legend 9 --output {out_path}/merge/{nosz_type}/taxonomy/{nosz_type}_{level}_rpkm --width 89 --height 95\n')
            plot.write(f'fi\n')
        
        # RPKM boxplot
        plot.write(f'if [ -f {out_path}/merge/{nosz_type}/{nosz_type}_merged_rpkm.txt ]; then\n')
        plot.write(f'  {software_dir}/Rscript {sub_dir}/gene_rpkm_boxplot.R --input {out_path}/merge/{nosz_type}/{nosz_type}_merged_rpkm.txt --group {group_list} --output {out_path}/merge/{nosz_type}/{nosz_type}_rpkm.pdf --width 160 --height 110\n')
        plot.write(f'fi\n')
        
        # Network plot
        plot.write(f'{software_dir}/Rscript {sub_dir}/network_plot.R --input {out_path}/merge/{nosz_type}/{nosz_type}_otutab.txt --group {group_list} --output {out_path}/merge/{nosz_type}/network --width 16 --height 11\n\n')
    
    plot.write('echo "Plotting analysis completed"\n')

os.system(f'sh {shell_path}/plot.sh')

# Generate summary report
with open(os.path.join(out_path, "analysis_summary.txt"), 'w') as report:
    report.write("=" * 70 + "\n")
    report.write("nosZ Gene Analysis Summary Report\n")
    report.write("=" * 70 + "\n\n")
    report.write(f"Analysis time: {os.popen('date').read().strip()}\n")
    report.write(f"Input directory: {input_dir}\n")
    report.write(f"Output directory: {out_path}\n")
    report.write(f"Number of samples: {len(valid_samples)}\n")
    report.write(f"Sample list: {', '.join(valid_samples)}\n\n")
    
    report.write("nosZ Gene Branch Analysis Parameters:\n")
    report.write("-" * 50 + "\n")
    for nosz_type, config in NOSZ_GENES.items():
        report.write(f"\n{nosz_type}:\n")
        report.write(f"  - Similarity threshold: {config['similarity']}%\n")
        report.write(f"  - Query coverage: {config['query_cover']}%\n")
        report.write(f"  - E-value threshold: {config['evalue']}\n")
        report.write(f"  - Clustering threshold: {config['cluster']}\n")
        report.write(f"  - Database: {config['database']}\n")
        
        report.write(f"\n  Sample statistics:\n")
        for samp in valid_samples:
            result_file = os.path.join(out_path, samp, f"{nosz_type}_{samp}.result.txt")
            if os.path.exists(result_file):
                with open(result_file, 'r') as rf:
                    content = rf.read().strip()
                    if content:
                        count = content.split('\t')[-1] if '\t' in content else "0"
                        report.write(f"    - {samp}: {count} sequences\n")
                    else:
                        report.write(f"    - {samp}: 0 sequences\n")
            else:
                report.write(f"    - {samp}: Not completed\n")
    
    report.write("\n" + "=" * 70 + "\n")
    report.write("Output File Description:\n")
    report.write("-" * 50 + "\n")
    report.write(f"1. Results for each sample: {out_path}/[sample_name]/\n")
    report.write(f"2. Merged results: {out_path}/merge/{nosz_type}/\n")
    report.write(f"3. Diversity analysis: {out_path}/merge/{nosz_type}/alpha/, beta/\n")
    report.write(f"4. Species classification: {out_path}/merge/{nosz_type}/taxonomy/\n")
    report.write(f"5. Visualization charts: PDF files in each analysis directory\n")
    report.write("=" * 70 + "\n")

print ("\n" + "=" * 70)
print ("nosZ Gene Analysis Pipeline Completed!")
print ("=" * 70)
print(f"Input directory: {input_dir}")
print(f"Results saved in: {out_path}")
print(f"Detailed report: {os.path.join(out_path, 'analysis_summary.txt')}")
print("\nAnalysis results for three nosZ branches:")
for nosz_type in NOSZ_GENES.keys():
    print(f"  - {nosz_type}: {out_path}/merge/{nosz_type}/")
print("=" * 70)
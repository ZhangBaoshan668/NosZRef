fa=$1
gene=$2
makeblastdb -in $fa -dbtype prot -out $gene
#blastx -db hzsA -query all_hzsA.fa -out hzsA_result_0.00001.txt -max_target_seqs 1 -outfmt '6 qseqid qlen sseqid sgi slen pident length mismatch gapopen qstart qend sstart send evalue bitscore staxid ssciname' -num_threads 20 -evalue 0.00001

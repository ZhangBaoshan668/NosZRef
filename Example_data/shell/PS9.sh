echo "=========================================="
echo "Processing sample: PS9"
echo "Input file: /project/wujp/zbs/wyy_0308/raw_data/PS9.fq.gz"
echo "=========================================="

echo "Step 1: Quality control"
/project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/software/fastp -i /project/wujp/zbs/wyy_0308/raw_data/PS9.fq.gz -o /project/wujp/zbs/wyy_0308/PS9/PS9.clean.fq.gz -w 16 -j /project/wujp/zbs/wyy_0308/PS9/PS9.json
echo -n "PS9" | paste - - <(jq '.summary.after_filtering.total_reads' /project/wujp/zbs/wyy_0308/PS9/PS9.json) | awk '{print $1 "	" $2}' > /project/wujp/zbs/wyy_0308/PS9/PS9_total_reads.txt

echo "Step 2: Convert to FASTA format"
/project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/software/seqtk seq -a /project/wujp/zbs/wyy_0308/PS9/PS9.clean.fq.gz > /project/wujp/zbs/wyy_0308/PS9/PS9.fa
awk 'BEGIN{FS=""; OFS=""; id=1} /^>/ {print ">PS9_"id++; next} {print}' /project/wujp/zbs/wyy_0308/PS9/PS9.fa > /project/wujp/zbs/wyy_0308/PS9/PS9.rename.fa

echo "=========================================="
echo "Processing nosZI (Similarity: 64%, Coverage: 75%)"
echo "=========================================="
/project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/software/diamond blastx -d /project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/database/nosZI.dmnd -q /project/wujp/zbs/wyy_0308/PS9/PS9.rename.fa -o /project/wujp/zbs/wyy_0308/PS9/nosZI_PS9.txt -e 1e-05 --id 64 --query-cover 75 -f 6 -p 140 -k 1
paste -d "	" <(echo -n "PS9") <(cat /project/wujp/zbs/wyy_0308/PS9/nosZI_PS9.txt | cut -f1 | sort | uniq | wc -l) > /project/wujp/zbs/wyy_0308/PS9/nosZI_PS9.result.txt
cat /project/wujp/zbs/wyy_0308/PS9/nosZI_PS9.txt | cut -f1 | sort | uniq > /project/wujp/zbs/wyy_0308/PS9/nosZI_PS9.id
/project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/software/seqtk subseq /project/wujp/zbs/wyy_0308/PS9/PS9.rename.fa /project/wujp/zbs/wyy_0308/PS9/nosZI_PS9.id > /project/wujp/zbs/wyy_0308/PS9/nosZI_PS9.target.fa
/project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/software/blastx -db /project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/database/nosZI -query /project/wujp/zbs/wyy_0308/PS9/nosZI_PS9.target.fa -out /project/wujp/zbs/wyy_0308/PS9/nosZI_PS9.tax_result.txt -max_target_seqs 1 -outfmt "6 qseqid qlen sseqid sgi slen pident length mismatch gapopen qstart qend sstart send evalue bitscore staxid ssciname" -num_threads 50 -evalue 1e-3
python3 /project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/sub/tax_statistics.py nosZI PS9 /project/wujp/zbs/wyy_0308/PS9/nosZI_PS9.tax_result.txt
# Calculate nosZI CPM/RPKM values
TOTAL_READS=$(cat /project/wujp/zbs/wyy_0308/PS9/PS9_total_reads.txt | cut -f2)
echo "Total reads: $TOTAL_READS"
python3 /project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/sub/calculate_cpm.py /project/wujp/zbs/wyy_0308/PS9 PS9 $TOTAL_READS nosZI 1920

echo "=========================================="
echo "Processing nosZII (Similarity: 61%, Coverage: 75%)"
echo "=========================================="
/project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/software/diamond blastx -d /project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/database/nosZII.dmnd -q /project/wujp/zbs/wyy_0308/PS9/PS9.rename.fa -o /project/wujp/zbs/wyy_0308/PS9/nosZII_PS9.txt -e 1e-05 --id 61 --query-cover 75 -f 6 -p 140 -k 1
paste -d "	" <(echo -n "PS9") <(cat /project/wujp/zbs/wyy_0308/PS9/nosZII_PS9.txt | cut -f1 | sort | uniq | wc -l) > /project/wujp/zbs/wyy_0308/PS9/nosZII_PS9.result.txt
cat /project/wujp/zbs/wyy_0308/PS9/nosZII_PS9.txt | cut -f1 | sort | uniq > /project/wujp/zbs/wyy_0308/PS9/nosZII_PS9.id
/project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/software/seqtk subseq /project/wujp/zbs/wyy_0308/PS9/PS9.rename.fa /project/wujp/zbs/wyy_0308/PS9/nosZII_PS9.id > /project/wujp/zbs/wyy_0308/PS9/nosZII_PS9.target.fa
/project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/software/blastx -db /project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/database/nosZII -query /project/wujp/zbs/wyy_0308/PS9/nosZII_PS9.target.fa -out /project/wujp/zbs/wyy_0308/PS9/nosZII_PS9.tax_result.txt -max_target_seqs 1 -outfmt "6 qseqid qlen sseqid sgi slen pident length mismatch gapopen qstart qend sstart send evalue bitscore staxid ssciname" -num_threads 50 -evalue 1e-3
python3 /project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/sub/tax_statistics.py nosZII PS9 /project/wujp/zbs/wyy_0308/PS9/nosZII_PS9.tax_result.txt
# Calculate nosZII CPM/RPKM values
TOTAL_READS=$(cat /project/wujp/zbs/wyy_0308/PS9/PS9_total_reads.txt | cut -f2)
echo "Total reads: $TOTAL_READS"
python3 /project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/sub/calculate_cpm.py /project/wujp/zbs/wyy_0308/PS9 PS9 $TOTAL_READS nosZII 2046

echo "=========================================="
echo "Processing nosZIII (Similarity: 77%, Coverage: 75%)"
echo "=========================================="
/project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/software/diamond blastx -d /project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/database/nosZIII.dmnd -q /project/wujp/zbs/wyy_0308/PS9/PS9.rename.fa -o /project/wujp/zbs/wyy_0308/PS9/nosZIII_PS9.txt -e 1e-05 --id 77 --query-cover 75 -f 6 -p 140 -k 1
paste -d "	" <(echo -n "PS9") <(cat /project/wujp/zbs/wyy_0308/PS9/nosZIII_PS9.txt | cut -f1 | sort | uniq | wc -l) > /project/wujp/zbs/wyy_0308/PS9/nosZIII_PS9.result.txt
cat /project/wujp/zbs/wyy_0308/PS9/nosZIII_PS9.txt | cut -f1 | sort | uniq > /project/wujp/zbs/wyy_0308/PS9/nosZIII_PS9.id
/project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/software/seqtk subseq /project/wujp/zbs/wyy_0308/PS9/PS9.rename.fa /project/wujp/zbs/wyy_0308/PS9/nosZIII_PS9.id > /project/wujp/zbs/wyy_0308/PS9/nosZIII_PS9.target.fa
/project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/software/blastx -db /project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/database/nosZIII -query /project/wujp/zbs/wyy_0308/PS9/nosZIII_PS9.target.fa -out /project/wujp/zbs/wyy_0308/PS9/nosZIII_PS9.tax_result.txt -max_target_seqs 1 -outfmt "6 qseqid qlen sseqid sgi slen pident length mismatch gapopen qstart qend sstart send evalue bitscore staxid ssciname" -num_threads 50 -evalue 1e-3
python3 /project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/sub/tax_statistics.py nosZIII PS9 /project/wujp/zbs/wyy_0308/PS9/nosZIII_PS9.tax_result.txt
# Calculate nosZIII CPM/RPKM values
TOTAL_READS=$(cat /project/wujp/zbs/wyy_0308/PS9/PS9_total_reads.txt | cut -f2)
echo "Total reads: $TOTAL_READS"
python3 /project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/sub/calculate_cpm.py /project/wujp/zbs/wyy_0308/PS9 PS9 $TOTAL_READS nosZIII 939

echo "Cleaning up temporary files"
rm -rf /project/wujp/zbs/wyy_0308/PS9/PS9.clean.fq.gz
rm -rf /project/wujp/zbs/wyy_0308/PS9/PS9.fa
rm -rf /project/wujp/zbs/wyy_0308/PS9/PS9.rename.fa
echo "Sample PS9 processing completed"

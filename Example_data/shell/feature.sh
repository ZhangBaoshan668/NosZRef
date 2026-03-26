#!/bin/bash
echo "Starting feature analysis (OTU clustering)"

echo "Processing nosZI OTU clustering"
sed -i "s/_[0-9][0-9]*$//" /project/wujp/zbs/wyy_0308/merge/nosZI/nosZI_merged_target.fa 2>/dev/null || true
/project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/software/usearch -fastx_uniques /project/wujp/zbs/wyy_0308/merge/nosZI/nosZI_merged_target.fa -fastaout /project/wujp/zbs/wyy_0308/merge/nosZI/nosZI_uniques.fa -sizeout -relabel OTU_ -minuniquesize 2
/project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/software/usearch -cluster_fast /project/wujp/zbs/wyy_0308/merge/nosZI/nosZI_uniques.fa -centroids /project/wujp/zbs/wyy_0308/merge/nosZI/nosZI_otus.fa -uc /project/wujp/zbs/wyy_0308/merge/nosZI/nosZI_clusters.uc -id 0.86 -minsize 2
/project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/software/vsearch --usearch_global /project/wujp/zbs/wyy_0308/merge/nosZI/nosZI_merged_target.fa --db /project/wujp/zbs/wyy_0308/merge/nosZI/nosZI_otus.fa --id 0.86 --threads 140 --otutabout /project/wujp/zbs/wyy_0308/merge/nosZI/nosZI_otutab.txt

echo "Processing nosZII OTU clustering"
sed -i "s/_[0-9][0-9]*$//" /project/wujp/zbs/wyy_0308/merge/nosZII/nosZII_merged_target.fa 2>/dev/null || true
/project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/software/usearch -fastx_uniques /project/wujp/zbs/wyy_0308/merge/nosZII/nosZII_merged_target.fa -fastaout /project/wujp/zbs/wyy_0308/merge/nosZII/nosZII_uniques.fa -sizeout -relabel OTU_ -minuniquesize 2
/project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/software/usearch -cluster_fast /project/wujp/zbs/wyy_0308/merge/nosZII/nosZII_uniques.fa -centroids /project/wujp/zbs/wyy_0308/merge/nosZII/nosZII_otus.fa -uc /project/wujp/zbs/wyy_0308/merge/nosZII/nosZII_clusters.uc -id 0.85 -minsize 2
/project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/software/vsearch --usearch_global /project/wujp/zbs/wyy_0308/merge/nosZII/nosZII_merged_target.fa --db /project/wujp/zbs/wyy_0308/merge/nosZII/nosZII_otus.fa --id 0.85 --threads 140 --otutabout /project/wujp/zbs/wyy_0308/merge/nosZII/nosZII_otutab.txt

echo "Processing nosZIII OTU clustering"
sed -i "s/_[0-9][0-9]*$//" /project/wujp/zbs/wyy_0308/merge/nosZIII/nosZIII_merged_target.fa 2>/dev/null || true
/project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/software/usearch -fastx_uniques /project/wujp/zbs/wyy_0308/merge/nosZIII/nosZIII_merged_target.fa -fastaout /project/wujp/zbs/wyy_0308/merge/nosZIII/nosZIII_uniques.fa -sizeout -relabel OTU_ -minuniquesize 2
/project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/software/usearch -cluster_fast /project/wujp/zbs/wyy_0308/merge/nosZIII/nosZIII_uniques.fa -centroids /project/wujp/zbs/wyy_0308/merge/nosZIII/nosZIII_otus.fa -uc /project/wujp/zbs/wyy_0308/merge/nosZIII/nosZIII_clusters.uc -id 0.86 -minsize 2
/project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/software/vsearch --usearch_global /project/wujp/zbs/wyy_0308/merge/nosZIII/nosZIII_merged_target.fa --db /project/wujp/zbs/wyy_0308/merge/nosZIII/nosZIII_otus.fa --id 0.86 --threads 140 --otutabout /project/wujp/zbs/wyy_0308/merge/nosZIII/nosZIII_otutab.txt

echo "Feature analysis completed"

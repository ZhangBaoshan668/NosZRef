#!/bin/bash
echo "Starting diversity analysis"

echo "Processing nosZI diversity analysis"
mkdir -p /project/wujp/zbs/wyy_0308/merge/nosZI/alpha /project/wujp/zbs/wyy_0308/merge/nosZI/beta /project/wujp/zbs/wyy_0308/merge/nosZI/network /project/wujp/zbs/wyy_0308/merge/nosZI/taxonomy
/project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/software/Rscript /project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/sub/otutab_rare.R --input /project/wujp/zbs/wyy_0308/merge/nosZI/nosZI_otutab.txt --normalize /project/wujp/zbs/wyy_0308/merge/nosZI/alpha/nosZI_otutab_rare.txt --output /project/wujp/zbs/wyy_0308/merge/nosZI/alpha/nosZI_alpha_div.txt
/project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/software/usearch -otutab_stats /project/wujp/zbs/wyy_0308/merge/nosZI/alpha/nosZI_otutab_rare.txt -output /project/wujp/zbs/wyy_0308/merge/nosZI/alpha/nosZI_otutab_rare.stat
/project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/software/usearch -alpha_div_rare /project/wujp/zbs/wyy_0308/merge/nosZI/alpha/nosZI_otutab_rare.txt -output /project/wujp/zbs/wyy_0308/merge/nosZI/alpha/nosZI_alpha_rare.txt -method without_replacement
sed -i "s/-/\t0.0/g" /project/wujp/zbs/wyy_0308/merge/nosZI/alpha/nosZI_alpha_rare.txt
/project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/software/usearch -beta_div /project/wujp/zbs/wyy_0308/merge/nosZI/alpha/nosZI_otutab_rare.txt -filename_prefix /project/wujp/zbs/wyy_0308/merge/nosZI/beta/
/project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/software/usearch -otutab_counts2freqs /project/wujp/zbs/wyy_0308/merge/nosZI/alpha/nosZI_otutab_rare.txt -output /project/wujp/zbs/wyy_0308/merge/nosZI/nosZI_otutab_freqs.txt

echo "Processing nosZII diversity analysis"
mkdir -p /project/wujp/zbs/wyy_0308/merge/nosZII/alpha /project/wujp/zbs/wyy_0308/merge/nosZII/beta /project/wujp/zbs/wyy_0308/merge/nosZII/network /project/wujp/zbs/wyy_0308/merge/nosZII/taxonomy
/project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/software/Rscript /project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/sub/otutab_rare.R --input /project/wujp/zbs/wyy_0308/merge/nosZII/nosZII_otutab.txt --normalize /project/wujp/zbs/wyy_0308/merge/nosZII/alpha/nosZII_otutab_rare.txt --output /project/wujp/zbs/wyy_0308/merge/nosZII/alpha/nosZII_alpha_div.txt
/project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/software/usearch -otutab_stats /project/wujp/zbs/wyy_0308/merge/nosZII/alpha/nosZII_otutab_rare.txt -output /project/wujp/zbs/wyy_0308/merge/nosZII/alpha/nosZII_otutab_rare.stat
/project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/software/usearch -alpha_div_rare /project/wujp/zbs/wyy_0308/merge/nosZII/alpha/nosZII_otutab_rare.txt -output /project/wujp/zbs/wyy_0308/merge/nosZII/alpha/nosZII_alpha_rare.txt -method without_replacement
sed -i "s/-/\t0.0/g" /project/wujp/zbs/wyy_0308/merge/nosZII/alpha/nosZII_alpha_rare.txt
/project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/software/usearch -beta_div /project/wujp/zbs/wyy_0308/merge/nosZII/alpha/nosZII_otutab_rare.txt -filename_prefix /project/wujp/zbs/wyy_0308/merge/nosZII/beta/
/project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/software/usearch -otutab_counts2freqs /project/wujp/zbs/wyy_0308/merge/nosZII/alpha/nosZII_otutab_rare.txt -output /project/wujp/zbs/wyy_0308/merge/nosZII/nosZII_otutab_freqs.txt

echo "Processing nosZIII diversity analysis"
mkdir -p /project/wujp/zbs/wyy_0308/merge/nosZIII/alpha /project/wujp/zbs/wyy_0308/merge/nosZIII/beta /project/wujp/zbs/wyy_0308/merge/nosZIII/network /project/wujp/zbs/wyy_0308/merge/nosZIII/taxonomy
/project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/software/Rscript /project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/sub/otutab_rare.R --input /project/wujp/zbs/wyy_0308/merge/nosZIII/nosZIII_otutab.txt --normalize /project/wujp/zbs/wyy_0308/merge/nosZIII/alpha/nosZIII_otutab_rare.txt --output /project/wujp/zbs/wyy_0308/merge/nosZIII/alpha/nosZIII_alpha_div.txt
/project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/software/usearch -otutab_stats /project/wujp/zbs/wyy_0308/merge/nosZIII/alpha/nosZIII_otutab_rare.txt -output /project/wujp/zbs/wyy_0308/merge/nosZIII/alpha/nosZIII_otutab_rare.stat
/project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/software/usearch -alpha_div_rare /project/wujp/zbs/wyy_0308/merge/nosZIII/alpha/nosZIII_otutab_rare.txt -output /project/wujp/zbs/wyy_0308/merge/nosZIII/alpha/nosZIII_alpha_rare.txt -method without_replacement
sed -i "s/-/\t0.0/g" /project/wujp/zbs/wyy_0308/merge/nosZIII/alpha/nosZIII_alpha_rare.txt
/project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/software/usearch -beta_div /project/wujp/zbs/wyy_0308/merge/nosZIII/alpha/nosZIII_otutab_rare.txt -filename_prefix /project/wujp/zbs/wyy_0308/merge/nosZIII/beta/
/project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/software/usearch -otutab_counts2freqs /project/wujp/zbs/wyy_0308/merge/nosZIII/alpha/nosZIII_otutab_rare.txt -output /project/wujp/zbs/wyy_0308/merge/nosZIII/nosZIII_otutab_freqs.txt

echo "Diversity analysis completed"

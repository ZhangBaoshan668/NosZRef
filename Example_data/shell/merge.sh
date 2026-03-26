#!/bin/bash
echo "Starting to merge all sample results"

echo "Merging nosZI results"
mkdir -p /project/wujp/zbs/wyy_0308/merge/nosZI
python3 /project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/sub/merge.py /project/wujp/zbs/wyy_0308 nosZI
echo "Merging nosZII results"
mkdir -p /project/wujp/zbs/wyy_0308/merge/nosZII
python3 /project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/sub/merge.py /project/wujp/zbs/wyy_0308 nosZII
echo "Merging nosZIII results"
mkdir -p /project/wujp/zbs/wyy_0308/merge/nosZIII
python3 /project/wujp/zbs/nosZ/ninth_paper_20260307/pipeline/final_pipeline/sub/merge.py /project/wujp/zbs/wyy_0308 nosZIII
echo "Merge completed"

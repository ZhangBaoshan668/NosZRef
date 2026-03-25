#!/usr/bin/python3
import sys
import os
import pandas as pd
from collections import defaultdict

# 定义基因特异性阈值 (放在文件开头便于维护)
GENE_THRESHOLDS = {
    "nosZI":{"genus":47.5,"species":81.45},
    "nosZII":{"genus":35.12,"species":80.08},
    "nosZIII":{"genus":48.49,"species":62.22}
}

def main():
    if len(sys.argv) < 4:
        print("Usage: python script.py <gene> <sample_id> <blast_results_file>")
        sys.exit(1)

    gene = sys.argv[1]
    sample_id = sys.argv[2]
    blast_results_file = sys.argv[3]
    sample_dir = os.path.dirname(blast_results_file)

    # 初始化分类计数器
    taxonomic_counts = {
        'Kingdom': defaultdict(int),
        'Phylum': defaultdict(int),  
        'Class': defaultdict(int),
        'Order': defaultdict(int),
        'Family': defaultdict(int),
        'Genus': defaultdict(int),
        'Species': defaultdict(int)
    }

    with open(blast_results_file, "r") as file:
        for line in file:
            if not line.strip():
                continue

            parts = line.strip().split("\t")
            if len(parts) < 6:
                continue

            try:
                similarity = float(parts[5].strip())
            except ValueError:
                continue

            # 解析分类信息
            current_taxonomic_info = parse_taxonomic_info(parts[2])
            
            # 应用基因特异性阈值
            apply_taxonomic_thresholds(gene, similarity, current_taxonomic_info)
            
            # 统计计数
            count_taxonomic_levels(current_taxonomic_info, taxonomic_counts)
    
    # 检查计数并应用 unclassified 条件
    apply_unclassified_condition(taxonomic_counts, 10)
    # 输出结果
    save_results(gene, sample_id, sample_dir, taxonomic_counts)

def parse_taxonomic_info(taxonomic_str):
    """解析分类信息字符串"""
    levels = {
        'd_': 'Kingdom',
        'p_': 'Phylum',
        'c_': 'Class',
        'o_': 'Order',
        'f_': 'Family',
        'g_': 'Genus',
        's_': 'Species'
    }
    
    current_info = {v: None for v in levels.values()}
    
    for level in taxonomic_str.split(";"):
        for prefix, tax_level in levels.items():
            if level.startswith(prefix):
                current_info[tax_level] = level[len(prefix):]
                break
                
    return current_info

def apply_taxonomic_thresholds(gene, similarity, tax_info):
    """应用基因特异性分类阈值"""
    thresholds = GENE_THRESHOLDS.get(gene, {})
    
    if not thresholds:
        return
        
    if similarity < thresholds.get("genus", float('inf')):
        tax_info['Genus'] = 'unclassified'
        tax_info['Species'] = 'unclassified'
    elif similarity < thresholds.get("species", float('inf')):
        tax_info['Species'] = 'unclassified'

def count_taxonomic_levels(tax_info, counters):
    """统计分类计数"""
    for level, taxon in tax_info.items():
        if taxon:
            counters[level][taxon] += 1

def apply_unclassified_condition(counters, threshold):
    """如果计数小于阈值，则标记为 unclassified"""
    for level, counts in counters.items():
        for taxon, count in list(counts.items()):
            if count < threshold:
                del counts[taxon]
                counts['unclassified'] += count
def save_results(gene, sample_id, output_dir, counters):
    """保存结果到CSV文件"""
    for tax_level, counts in counters.items():
        df = pd.DataFrame(
            [[sample_id, taxon, count] for taxon, count in counts.items()],
            columns=['Sample ID', 'Taxon', 'Count']
        )
        output_file = os.path.join(
            output_dir, 
            f"{gene}_{sample_id}_{tax_level.lower()}_counts.csv"
        )
        df.to_csv(output_file, index=False)

if __name__ == "__main__":
    main()
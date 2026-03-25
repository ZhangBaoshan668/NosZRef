#!/usr/bin/python3
import os
import sys

def em_algorithm(nA, nB, nAB, epsilon=1e-6):
    """EM算法分配重叠序列"""
    N = nA + nB + nAB
    if N == 0:
        return nA, nB
    
    thetaA = 0.5
    while True:
        p = thetaA / (thetaA + (1 - thetaA))
        new_thetaA = (nA + nAB * p) / N
        if abs(new_thetaA - thetaA) < epsilon:
            break
        thetaA = new_thetaA
    
    return nA + nAB * thetaA, nB + nAB * (1 - thetaA)

def process_sample(samp_path, samp):
    """处理单个样本的重叠分配"""
    # 定义文件路径
    nosZI_file = os.path.join(samp_path, f"nosZI_{samp}.txt")
    nosZII_file = os.path.join(samp_path, f"nosZII_{samp}.txt")
    
    # 检查文件是否存在
    if not os.path.exists(nosZI_file) or not os.path.exists(nosZII_file):
        return
    
    # 提取第一列序列ID
    nosZI_ids = set()
    nosZII_ids = set()
    
    with open(nosZI_file, 'r') as f:
        for line in f:
            if line.strip():
                nosZI_ids.add(line.split('\t')[0])
    
    with open(nosZII_file, 'r') as f:
        for line in f:
            if line.strip():
                nosZII_ids.add(line.split('\t')[0])
    
    # 计算统计量
    nA = len(nosZI_ids - nosZII_ids)
    nB = len(nosZII_ids - nosZI_ids)
    nAB = len(nosZI_ids & nosZII_ids)
    
    if nAB == 0:
        return
    
    # EM算法分配
    countA, countB = em_algorithm(nA, nB, nAB)
    
    # 更新result文件
    for gene, count in [('nosZI', countA), ('nosZII', countB)]:
        result_file = os.path.join(samp_path, f"{gene}_{samp}.result.txt")
        if os.path.exists(result_file):
            with open(result_file, 'r') as f:
                parts = f.read().strip().split('\t')
            if len(parts) >= 2:
                with open(result_file, 'w') as f:
                    f.write(f"{parts[0]}\t{count:.0f}\n")
    
    print(f"  样本 {samp}: nosZI={countA:.0f}, nosZII={countB:.0f} (重叠:{nAB})")

def main():
    output_dir = sys.argv[1]
    
    # 遍历所有样本目录
    for item in os.listdir(output_dir):
        samp_path = os.path.join(output_dir, item)
        if os.path.isdir(samp_path) and item not in ['raw_data', 'shell', 'merge']:
            process_sample(samp_path, item)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 allocate_overlap.py <output_dir>")
        sys.exit(1)
    main()
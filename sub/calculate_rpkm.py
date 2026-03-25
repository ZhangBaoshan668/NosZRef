#!/usr/bin/python3
import sys
import os

def calculate_rpkm(total_reads_file, result_file, gene_length, output_dir, gene_name):
    """
    计算RPKM值
    RPKM = (reads_count / total_reads) * 1e9 / gene_length
    
    参数:
        total_reads_file: 总读数文件路径
        result_file: 结果文件路径（包含样本名和序列数）
        gene_length: 基因长度（整数）
        output_dir: 输出目录
        gene_name: 基因名称
    """
    try:
        # 读取总读数
        with open(total_reads_file, 'r') as total_f:
            line = total_f.readline().strip()
            if not line:
                print(f"错误: {total_reads_file} 文件为空")
                return
            total_reads = int(line.split()[1])
        
        if total_reads == 0:
            print(f"警告: 总读数为0，无法计算RPKM")
            return
        
        # 提取结果文件中的样本名和序列读数
        sample_name = None
        reads = 0
        
        with open(result_file, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 2:
                    sample_name = parts[0]
                    reads = int(parts[1])
                    break  # 只读取第一行
        
        if sample_name is None:
            print(f"错误: 无法从 {result_file} 读取样本名")
            return
        
        if reads == 0:
            print(f"警告: 基因 {gene_name} 在 {result_file} 中未找到序列，RPKM设为0")
            rpkm = 0
        else:
            # 计算RPKM
            rpkm = (reads / total_reads) * 1e9 / gene_length
        
        # 构建输出文件路径
        output_file_path = os.path.join(output_dir, f"{gene_name}_{sample_name}.rpkm.txt")
        
        # 将结果写入文件
        with open(output_file_path, 'w') as out_f:
            out_f.write("SampleID\tRPKM\n")
            out_f.write(f"{sample_name}\t{rpkm:.6f}\n")
        
        print(f"成功: {gene_name} RPKM = {rpkm:.6f} (样本: {sample_name}, 读数: {reads}, 总读数: {total_reads}, 基因长度: {gene_length})")
        
    except FileNotFoundError as e:
        print(f"错误: 文件不存在 - {e}")
    except ValueError as e:
        print(f"错误: 数据格式错误 - {e}")
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python calculate_rpkm.py <total_reads_file> <result_file> <gene_length> <output_dir> <gene_name>")
        print("示例: python calculate_rpkm.py sample_total_reads.txt nosZII_sample.result.txt 1200 output_dir nosZII")
        sys.exit(1)

    total_reads_file = sys.argv[1]
    result_file = sys.argv[2]
    gene_length = int(sys.argv[3])  # 直接使用数字参数
    output_dir = sys.argv[4]
    gene_name = sys.argv[5]

    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    calculate_rpkm(total_reads_file, result_file, gene_length, output_dir, gene_name)
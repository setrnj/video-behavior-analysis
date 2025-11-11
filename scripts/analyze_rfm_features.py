#!/usr/bin/env python3
"""
分析 RFM 数据的分布特征，为后续建模提供依据
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- 配置 ---
INPUT_CSV_PATH = '../results/rfm_data_for_clustering.csv'
OUTPUT_DIR = '../docs/analysis/'

def analyze_features():
    print(f"读取 RFM 数据: {INPUT_CSV_PATH}")
    df = pd.read_csv(INPUT_CSV_PATH)
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    print("数据基本信息:")
    print(df.describe())
    df.describe().to_csv(f"{OUTPUT_DIR}/rfm_summary_stats.csv")
    
    print("\n绘制各维度分布直方图...")
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    sns.histplot(df['recency'], bins=30, kde=True, ax=axes[0])
    axes[0].set_title('Recency Distribution')
    sns.histplot(df['frequency'], bins=30, kde=True, ax=axes[1])
    axes[1].set_title('Frequency Distribution')
    sns.histplot(df['monetary'], bins=30, kde=True, ax=axes[2])
    axes[2].set_title('Monetary Distribution')
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/rfm_distributions.png")
    plt.close()
    print(f"分布图已保存至 {OUTPUT_DIR}/rfm_distributions.png")

    print("\n绘制 RFM 相关性热力图...")
    corr_matrix = df[['recency', 'frequency', 'monetary']].corr()
    plt.figure(figsize=(6, 5))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('RFM Correlation Heatmap')
    plt.savefig(f"{OUTPUT_DIR}/rfm_correlation.png")
    plt.close()
    print(f"相关性热力图已保存至 {OUTPUT_DIR}/rfm_correlation.png")

    print("\n分析完成。")

if __name__ == "__main__":
    analyze_features()

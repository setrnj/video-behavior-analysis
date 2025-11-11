#!/usr/bin/env python3
"""
A/B 测试: 比较 K-Means 聚类 与 原始规则分群 的效果
由于没有明确的“真实标签”，我们通过轮廓系数(Silhouette Score)来评估内部一致性
"""

import pandas as pd
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import numpy as np

# --- 配置 ---
KMEANS_CSV_PATH = '../results/rfm_kmeans_clusters.csv'
HIVE_RFM_CSV_PATH = '../results/rfm_data_for_clustering.csv' # 包含原始 RFM 值
OUTPUT_REPORT_PATH = '../results/clustering_comparison_report.txt'

def compare_methods():
    print("读取 K-Means 聚类结果...")
    df_kmeans = pd.read_csv(KMEANS_CSV_PATH)
    print("读取原始 RFM 数据...")
    df_original = pd.read_csv(HIVE_RFM_CSV_PATH)
    
    # 确保两个 dataframe 按 user_key 排序一致
    df_kmeans.sort_values(by='user_key', inplace=True)
    df_original.sort_values(by='user_key', inplace=True)
    
    # 准备数据用于评估
    features = ['recency', 'frequency', 'monetary']
    X_original = df_original[features]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_original)
    
    # 获取两种方法的标签
    labels_kmeans = df_kmeans['cluster'].values
    # 为原始规则分群打标签 (模拟原始逻辑)
    def assign_rule_label(row):
        r, f, m = row['recency'], row['frequency'], row['monetary']
        if r <= 7 and f >= 5 and m >= 100: return 0 # 活跃高价值
        elif r <= 14 and f >= 3: return 1 # 活跃一般
        elif r > 30 and f < 2: return 2 # 流失风险
        else: return 3 # 其他
    labels_rule = df_original.apply(assign_rule_label, axis=1).values
    
    # 计算 Silhouette Score
    score_kmeans = silhouette_score(X_scaled, labels_kmeans)
    score_rule = silhouette_score(X_scaled, labels_rule)
    
    print(f"\n--- 聚类效果比较 (Silhouette Score) ---")
    print(f"K-Means 聚类得分: {score_kmeans:.4f}")
    print(f"规则分群得分: {score_rule:.4f}")
    
    with open(OUTPUT_REPORT_PATH, 'w') as f:
        f.write("--- 聚类效果比较 (Silhouette Score) ---\n")
        f.write(f"K-Means 聚类得分: {score_kmeans:.4f}\n")
        f.write(f"规则分群得分: {score_rule:.4f}\n")
        if score_kmeans > score_rule:
            f.write("结论: K-Means 聚类效果优于规则分群。\n")
            print("结论: K-Means 聚类效果优于规则分群。")
        else:
            f.write("结论: 规则分群效果优于或等于 K-Means 聚类。\n")
            print("结论: 规则分群效果优于或等于 K-Means 聚类。")
            
    print(f"\n比较报告已保存至 {OUTPUT_REPORT_PATH}")

if __name__ == "__main__":
    compare_methods()

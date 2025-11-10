#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户分群与聚类结果图表生成脚本
图表7: K-means聚类结果散点图
图表8: 分群用户特征雷达图
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import os

def setup_english_fonts():
    """设置英文字体"""
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['font.size'] = 10

def generate_kmeans_clustering():
    """生成K-means聚类结果散点图"""
    setup_english_fonts()
    
    # 生成RFM数据
    np.random.seed(42)
    n_users = 800
    
    # 创建4个不同的用户群体
    cluster_centers = np.array([
        [5, 8, 200],   # 高价值用户：R小，F大，M大
        [20, 2, 50],   # 流失风险：R大，F小，M小
        [8, 4, 120],   # 普通用户
        [2, 10, 300]   # 忠诚用户
    ])
    
    # 为每个集群生成数据
    data = []
    for i, center in enumerate(cluster_centers):
        cluster_size = n_users // 4
        cluster_data = np.random.normal(center, [2, 1.5, 30], (cluster_size, 3))
        cluster_data = np.clip(cluster_data, [0, 0, 0], [30, 15, 500])  # 限制范围
        data.append(np.column_stack([cluster_data, np.full(cluster_size, i)]))
    
    # 合并所有数据
    all_data = np.vstack(data)
    rfm_df = pd.DataFrame(all_data, columns=['Recency', 'Frequency', 'Monetary', 'True_Cluster'])
    
    # 标准化数据
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm_df[['Recency', 'Frequency', 'Monetary']])
    
    # 应用K-means聚类
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(rfm_scaled)
    rfm_df['Cluster'] = clusters
    
    # 计算轮廓系数
    silhouette_avg = silhouette_score(rfm_scaled, clusters)
    
    # 创建聚类结果图
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # 子图1: 实际聚类结果
    colors = ['red', 'blue', 'green', 'orange']
    cluster_names = ['High Value', 'Churn Risk', 'Regular', 'Loyal']
    
    for i in range(4):
        mask = rfm_df['True_Cluster'] == i
        axes[0].scatter(rfm_df.loc[mask, 'Recency'], rfm_df.loc[mask, 'Monetary'],
                       c=colors[i], label=cluster_names[i], alpha=0.7, s=30)
    
    # 标记真实中心点
    for i, center in enumerate(cluster_centers):
        axes[0].scatter(center[0], center[2], c=colors[i], marker='*', s=200, 
                       edgecolors='black', linewidth=1)
    
    axes[0].set_xlabel('Recency (Days)')
    axes[0].set_ylabel('Monetary (Minutes)')
    axes[0].set_title('True User Clusters (Ground Truth)')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # 子图2: K-means聚类结果
    for i in range(4):
        mask = rfm_df['Cluster'] == i
        axes[1].scatter(rfm_df.loc[mask, 'Recency'], rfm_df.loc[mask, 'Monetary'],
                       c=colors[i], label=f'Cluster {i+1}', alpha=0.7, s=30)
    
    # 标记K-means中心点
    cluster_centers_original = scaler.inverse_transform(kmeans.cluster_centers_)
    for i, center in enumerate(cluster_centers_original):
        axes[1].scatter(center[0], center[2], c=colors[i], marker='D', s=150, 
                       edgecolors='black', linewidth=1)
    
    axes[1].set_xlabel('Recency (Days)')
    axes[1].set_ylabel('Monetary (Minutes)')
    axes[1].set_title(f'K-means Clustering Results\n(Silhouette Score: {silhouette_avg:.3f})')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # 保存图表
    os.makedirs('docs/clustering', exist_ok=True)
    plt.savefig("docs/clustering/kmeans_clustering.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ K-means聚类结果图已生成: docs/clustering/kmeans_clustering.png")

def generate_radar_chart():
    """生成分群用户特征雷达图"""
    setup_english_fonts()
    
    # 生成聚类数据
    np.random.seed(42)
    
    # 定义4个用户群体的特征
    cluster_profiles = {
        'High Value': {'R': 0.9, 'F': 0.95, 'M': 0.98, 'Activity': 0.92, 'Loyalty': 0.88},
        'Loyal': {'R': 0.85, 'F': 0.9, 'M': 0.85, 'Activity': 0.88, 'Loyalty': 0.95},
        'Regular': {'R': 0.6, 'F': 0.7, 'M': 0.65, 'Activity': 0.75, 'Loyalty': 0.6},
        'Churn Risk': {'R': 0.3, 'F': 0.4, 'M': 0.35, 'Activity': 0.45, 'Loyalty': 0.25}
    }
    
    # 雷达图设置
    categories = list(cluster_profiles['High Value'].keys())
    N = len(categories)
    
    # 计算角度
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # 闭合图形
    
    # 创建雷达图
    fig, ax = plt.subplots(figsize=(12, 10), subplot_kw=dict(projection='polar'))
    
    # 定义颜色
    colors = ['red', 'blue', 'green', 'orange']
    
    # 绘制每个群体的雷达图
    for i, (cluster_name, profile) in enumerate(cluster_profiles.items()):
        values = list(profile.values())
        values += values[:1]  # 闭合图形
        
        ax.plot(angles, values, 'o-', linewidth=2, label=cluster_name, color=colors[i])
        ax.fill(angles, values, alpha=0.1, color=colors[i])
    
    # 设置角度标签
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=11)
    
    # 设置径向标签
    ax.set_rlabel_position(30)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], fontsize=9)
    ax.set_ylim(0, 1.1)
    
    # 添加标题和图例
    plt.title('User Cluster Profiles Radar Chart', size=14, y=1.08)
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    
    # 保存图表
    os.makedirs('docs/clustering', exist_ok=True)
    plt.savefig("docs/clustering/cluster_radar_chart.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ 用户分群雷达图已生成: docs/clustering/cluster_radar_chart.png")

if __name__ == "__main__":
    generate_kmeans_clustering()
    generate_radar_chart()

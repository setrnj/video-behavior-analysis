#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成所有可视化图表
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import subprocess
import numpy as np
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 创建输出目录
output_dir = '/root/video-behavior-analysis/video-behavior-analysis-system/docs'
os.makedirs(output_dir, exist_ok=True)

print("=== 开始生成可视化图表 ===")

# 1. 生成用户分群图
print("1. 生成用户分群图...")
try:
    # 从HDFS获取RFM数据
    subprocess.run(["hdfs", "dfs", "-get", "/results/user_rfm/000000_0", "rfm_data.csv"])
    
    # 读取数据
    df = pd.read_csv('rfm_data.csv', header=None, names=['user_key', 'recency', 'frequency', 'monetary'])
    
    # K-means聚类
    from sklearn.cluster import KMeans
    kmeans = KMeans(n_clusters=4, random_state=42)
    df['cluster'] = kmeans.fit_predict(df[['recency', 'frequency', 'monetary']])
    
    # 创建图表
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # RFM散点图
    axes[0, 0].scatter(df['recency'], df['monetary'], c=df['cluster'], cmap='viridis', alpha=0.6)
    axes[0, 0].set_xlabel('最近活跃度')
    axes[0, 0].set_ylabel('观看时长')
    axes[0, 0].set_title('用户聚类分布 (R-M)')
    
    # 频次-价值散点图
    axes[0, 1].scatter(df['frequency'], df['monetary'], c=df['cluster'], cmap='viridis', alpha=0.6)
    axes[0, 1].set_xlabel('观看频次')
    axes[0, 1].set_ylabel('观看时长')
    axes[0, 1].set_title('用户聚类分布 (F-M)')
    
    # 聚类分布饼图
    cluster_counts = df['cluster'].value_counts()
    axes[1, 0].pie(cluster_counts.values, labels=[f'聚类{i}' for i in cluster_counts.index], 
                   autopct='%1.1f%%', startangle=90)
    axes[1, 0].set_title('用户分群比例')
    
    # 特征对比
    cluster_means = df.groupby('cluster')[['recency', 'frequency', 'monetary']].mean()
    for i, (cluster, values) in enumerate(cluster_means.iterrows()):
        axes[1, 1].plot(['R', 'F', 'M'], values.values, marker='o', label=f'聚类{cluster}', linewidth=2)
    
    axes[1, 1].set_title('各分群RFM特征对比')
    axes[1, 1].legend()
    axes[1, 1].grid(True)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/user_segmentation.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ 用户分群图已保存")
    
except Exception as e:
    print(f"❌ 用户分群图生成失败: {e}")

# 2. 生成时段热力图
print("2. 生成时段热力图...")
try:
    # 生成模拟热力图数据
    hours = list(range(24))
    days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    
    np.random.seed(42)
    heatmap_data = np.random.poisson(100, (7, 24))
    
    # 创建热力图
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(heatmap_data, 
                xticklabels=hours,
                yticklabels=days,
                cmap='YlOrRd',
                annot=True,
                fmt='d',
                cbar_kws={'label': '观看次数'})
    
    ax.set_title('用户观看行为时段热力图', fontsize=16, fontweight='bold')
    ax.set_xlabel('小时', fontsize=12)
    ax.set_ylabel('星期', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/hourly_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ 时段热力图已保存")
    
except Exception as e:
    print(f"❌ 时段热力图生成失败: {e}")

# 3. 生成留存曲线
print("3. 生成留存曲线...")
try:
    # 模拟留存数据
    periods = [1, 3, 7, 14, 30]
    retention_rates = [100, 85, 70, 55, 40]
    
    # 创建留存曲线
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(periods, retention_rates, 'o-', linewidth=2, markersize=8, color='#2E86AB')
    ax.fill_between(periods, retention_rates, alpha=0.3, color='#2E86AB')
    
    ax.set_title('用户留存曲线', fontsize=16, fontweight='bold')
    ax.set_xlabel('留存天数', fontsize=12)
    ax.set_ylabel('留存率 (%)', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 100)
    
    # 添加数据标签
    for i, (period, rate) in enumerate(zip(periods, retention_rates)):
        ax.annotate(f'{rate}%', (period, rate), 
                   textcoords="offset points", xytext=(0,10), ha='center')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/retention_curve.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ 留存曲线已保存")
    
except Exception as e:
    print(f"❌ 留存曲线生成失败: {e}")

# 4. 生成RFM分布图
print("4. 生成RFM分布图...")
try:
    # 模拟RFM数据
    np.random.seed(42)
    n_users = 1000
    
    rfm_data = {
        'Recency': np.random.normal(15, 10, n_users),
        'Frequency': np.random.poisson(5, n_users),
        'Monetary': np.random.exponential(100, n_users)
    }
    
    df_rfm = pd.DataFrame(rfm_data)
    
    # 创建子图
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # R分布
    axes[0, 0].hist(df_rfm['Recency'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
    axes[0, 0].set_title('最近活跃度分布 (R)', fontweight='bold')
    axes[0, 0].set_xlabel('天数')
    axes[0, 0].set_ylabel('用户数量')
    
    # F分布
    axes[0, 1].hist(df_rfm['Frequency'], bins=20, alpha=0.7, color='lightgreen', edgecolor='black')
    axes[0, 1].set_title('观看频次分布 (F)', fontweight='bold')
    axes[0, 1].set_xlabel('次数')
    axes[0, 1].set_ylabel('用户数量')
    
    # M分布
    axes[1, 0].hist(df_rfm['Monetary'], bins=30, alpha=0.7, color='salmon', edgecolor='black')
    axes[1, 0].set_title('观看时长分布 (M)', fontweight='bold')
    axes[1, 0].set_xlabel('分钟')
    axes[1, 0].set_ylabel('用户数量')
    
    # RFM相关性
    correlation = df_rfm.corr()
    im = axes[1, 1].imshow(correlation, cmap='coolwarm', aspect='auto')
    axes[1, 1].set_xticks(range(len(correlation.columns)))
    axes[1, 1].set_yticks(range(len(correlation.columns)))
    axes[1, 1].set_xticklabels(correlation.columns)
    axes[1, 1].set_yticklabels(correlation.columns)
    axes[1, 1].set_title('RFM相关性矩阵', fontweight='bold')
    
    # 添加相关系数标签
    for i in range(len(correlation.columns)):
        for j in range(len(correlation.columns)):
            axes[1, 1].text(j, i, f'{correlation.iloc[i, j]:.2f}',
                          ha="center", va="center", color="black")
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/rfm_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ RFM分布图已保存")
    
except Exception as e:
    print(f"❌ RFM分布图生成失败: {e}")

print("\n=== 所有图表生成完成 ===")
print(f"图表保存位置: {output_dir}")
print("生成的文件:")
os.system(f"ls -la {output_dir}/*.png")

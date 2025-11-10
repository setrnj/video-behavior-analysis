#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
import subprocess
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 从HDFS获取数据
print("从HDFS获取RFM数据...")
subprocess.run(["hdfs", "dfs", "-get", "/results/user_rfm/000000_0", "rfm_data.csv"])

# 读取数据
df = pd.read_csv('rfm_data.csv', header=None, names=['user_key', 'recency', 'frequency', 'monetary'])
print(f"加载数据: {len(df)} 条记录")

# K-means聚类
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
plt.savefig('/root/video-behavior-analysis/video-behavior-analysis-system/docs/user_segmentation.png', dpi=300, bbox_inches='tight')
plt.close()

print("用户分群图表已保存到 /root/video-behavior-analysis/video-behavior-analysis-system/docs/user_segmentation.png")

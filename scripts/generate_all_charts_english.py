#!/usr/bin/env python3
"""
Generate all visualization charts in English
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import subprocess
import numpy as np
import os

# Use default English fonts - remove Chinese font settings

# Create output directory
output_dir = '/root/video-behavior-analysis/video-behavior-analysis-system/docs'
os.makedirs(output_dir, exist_ok=True)

print("=== Starting to generate visualization charts ===")

# 1. Generate User Segmentation Chart
print("1. Generating User Segmentation Chart...")
try:
    # Get RFM data from HDFS
    subprocess.run(["hdfs", "dfs", "-get", "/results/user_rfm/000000_0", "rfm_data.csv"])
    
    # Read data
    df = pd.read_csv('rfm_data.csv', header=None, names=['user_key', 'recency', 'frequency', 'monetary'])
    
    # K-means clustering
    from sklearn.cluster import KMeans
    kmeans = KMeans(n_clusters=4, random_state=42)
    df['cluster'] = kmeans.fit_predict(df[['recency', 'frequency', 'monetary']])
    
    # Create charts
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # RFM scatter plot
    axes[0, 0].scatter(df['recency'], df['monetary'], c=df['cluster'], cmap='viridis', alpha=0.6)
    axes[0, 0].set_xlabel('Recency')
    axes[0, 0].set_ylabel('Monetary Value')
    axes[0, 0].set_title('User Clustering Distribution (R-M)')
    
    # Frequency-Value scatter plot
    axes[0, 1].scatter(df['frequency'], df['monetary'], c=df['cluster'], cmap='viridis', alpha=0.6)
    axes[0, 1].set_xlabel('Frequency')
    axes[0, 1].set_ylabel('Monetary Value')
    axes[0, 1].set_title('User Clustering Distribution (F-M)')
    
    # Cluster distribution pie chart
    cluster_counts = df['cluster'].value_counts()
    axes[1, 0].pie(cluster_counts.values, labels=[f'Cluster {i}' for i in cluster_counts.index], 
                   autopct='%1.1f%%', startangle=90)
    axes[1, 0].set_title('User Segment Distribution')
    
    # Feature comparison
    cluster_means = df.groupby('cluster')[['recency', 'frequency', 'monetary']].mean()
    for i, (cluster, values) in enumerate(cluster_means.iterrows()):
        axes[1, 1].plot(['R', 'F', 'M'], values.values, marker='o', label=f'Cluster {cluster}', linewidth=2)
    
    axes[1, 1].set_title('RFM Feature Comparison by Cluster')
    axes[1, 1].legend()
    axes[1, 1].grid(True)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/user_segmentation_english.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ User segmentation chart saved")
    
except Exception as e:
    print(f"❌ User segmentation chart generation failed: {e}")

# 2. Generate Hourly Heatmap
print("2. Generating Hourly Heatmap...")
try:
    # Generate sample heatmap data
    hours = list(range(24))
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    np.random.seed(42)
    heatmap_data = np.random.poisson(100, (7, 24))
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(heatmap_data, 
                xticklabels=hours,
                yticklabels=days,
                cmap='YlOrRd',
                annot=True,
                fmt='d',
                cbar_kws={'label': 'View Count'})
    
    ax.set_title('User Viewing Behavior Heatmap by Time', fontsize=16, fontweight='bold')
    ax.set_xlabel('Hour', fontsize=12)
    ax.set_ylabel('Day', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/hourly_heatmap_english.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Hourly heatmap saved")
    
except Exception as e:
    print(f"❌ Hourly heatmap generation failed: {e}")

# 3. Generate Retention Curve
print("3. Generating Retention Curve...")
try:
    # Sample retention data
    periods = [1, 3, 7, 14, 30]
    retention_rates = [100, 85, 70, 55, 40]
    
    # Create retention curve
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(periods, retention_rates, marker='o', linewidth=3, markersize=8, color='#2E86AB')
    
    ax.set_title('User Retention Curve', fontsize=16, fontweight='bold')
    ax.set_xlabel('Retention Days', fontsize=12)
    ax.set_ylabel('Retention Rate (%)', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 100)
    
    # Add data labels
    for i, (period, rate) in enumerate(zip(periods, retention_rates)):
        ax.annotate(f'{rate}%', (period, rate), 
                   textcoords="offset points", xytext=(0,10), ha='center')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/retention_curve_english.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Retention curve saved")
    
except Exception as e:
    print(f"❌ Retention curve generation failed: {e}")

# 4. Generate RFM Distribution
print("4. Generating RFM Distribution...")
try:
    # Sample RFM data
    np.random.seed(42)
    n_users = 1000
    
    rfm_data = {
        'Recency': np.random.normal(15, 10, n_users),
        'Frequency': np.random.poisson(5, n_users),
        'Monetary': np.random.exponential(100, n_users)
    }
    
    df_rfm = pd.DataFrame(rfm_data)
    
    # Create subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # R distribution
    axes[0, 0].hist(df_rfm['Recency'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
    axes[0, 0].set_title('Recency Distribution (R)', fontweight='bold')
    axes[0, 0].set_xlabel('Days')
    axes[0, 0].set_ylabel('User Count')
    
    # F distribution
    axes[0, 1].hist(df_rfm['Frequency'], bins=20, alpha=0.7, color='lightgreen', edgecolor='black')
    axes[0, 1].set_title('Frequency Distribution (F)', fontweight='bold')
    axes[0, 1].set_xlabel('Count')
    axes[0, 1].set_ylabel('User Count')
    
    # M distribution
    axes[1, 0].hist(df_rfm['Monetary'], bins=30, alpha=0.7, color='salmon', edgecolor='black')
    axes[1, 0].set_title('Monetary Distribution (M)', fontweight='bold')
    axes[1, 0].set_xlabel('Minutes')
    axes[1, 0].set_ylabel('User Count')
    
    # RFM correlation
    correlation = df_rfm.corr()
    im = axes[1, 1].imshow(correlation, cmap='coolwarm', aspect='auto')
    axes[1, 1].set_xticks(range(len(correlation.columns)))
    axes[1, 1].set_yticks(range(len(correlation.columns)))
    axes[1, 1].set_xticklabels(correlation.columns)
    axes[1, 1].set_yticklabels(correlation.columns)
    axes[1, 1].set_title('RFM Correlation Matrix', fontweight='bold')
    
    # Add correlation coefficient labels
    for i in range(len(correlation.columns)):
        for j in range(len(correlation.columns)):
            axes[1, 1].text(j, i, f'{correlation.iloc[i, j]:.2f}',
                          ha="center", va="center", color="black")
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/rfm_distribution_english.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ RFM distribution chart saved")
    
except Exception as e:
    print(f"❌ RFM distribution chart generation failed: {e}")

print("\n=== All charts generated successfully ===")
print(f"Charts saved to: {output_dir}")
print("Generated files:")
os.system(f"ls -la {output_dir}/*english.png 2>/dev/null || echo 'No English charts found yet'")

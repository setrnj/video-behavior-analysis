#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
效果验证与趋势分析图表生成脚本
图表9: 用户留存曲线图
图表10: 策略效果对比图
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

def setup_english_fonts():
    """设置英文字体"""
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['font.size'] = 10

def generate_retention_curves():
    """生成用户留存曲线图"""
    setup_english_fonts()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # 模拟留存数据
    days = np.arange(1, 31)
    
    # 不同用户分群的留存率
    retention_data = {
        'High Value': np.exp(-days/30) * 0.8 + 0.1,
        'Medium Value': np.exp(-days/20) * 0.7 + 0.1,
        'Low Value': np.exp(-days/10) * 0.6 + 0.1,
        'New Users': np.exp(-days/15) * 0.5 + 0.1
    }
    
    # 绘制留存曲线
    colors = ['#2E8B57', '#4169E1', '#FF6347', '#9370DB']
    for i, (group, retention) in enumerate(retention_data.items()):
        ax1.plot(days, retention * 100, label=group, color=colors[i], linewidth=2.5, marker='o', markersize=4)
    
    ax1.set_xlabel('Days After Registration', fontsize=12)
    ax1.set_ylabel('Retention Rate (%)', fontsize=12)
    ax1.set_title('User Retention Curves by Segment', fontsize=14, pad=15)
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 100)
    
    # 绘制留存率热力图（月度）
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    segments = ['High Value', 'Medium Value', 'Low Value', 'New Users']
    
    # 模拟月度留存数据
    monthly_retention = np.random.rand(len(segments), len(months)) * 40 + 30
    monthly_retention[0, :] += 20  # 高价值用户留存率更高
    monthly_retention[3, :] -= 15  # 新用户留存率较低
    
    im = ax2.imshow(monthly_retention, cmap='YlGnBu', aspect='auto')
    
    # 设置坐标轴标签
    ax2.set_xticks(np.arange(len(months)))
    ax2.set_yticks(np.arange(len(segments)))
    ax2.set_xticklabels(months, fontsize=10)
    ax2.set_yticklabels(segments, fontsize=10)
    
    # 在热力图中显示数值
    for i in range(len(segments)):
        for j in range(len(months)):
            ax2.text(j, i, f'{monthly_retention[i, j]:.1f}%', 
                    ha="center", va="center", color="black", fontsize=9)
    
    ax2.set_title('Monthly Retention Rate Heatmap (%)', fontsize=14, pad=15)
    
    # 添加颜色条
    cbar = plt.colorbar(im, ax=ax2, shrink=0.8)
    cbar.set_label('Retention Rate (%)', fontsize=10)
    
    plt.tight_layout()
    
    # 保存图表
    os.makedirs('docs/validation', exist_ok=True)
    plt.savefig("docs/validation/retention_curves.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ 用户留存曲线图已生成: docs/validation/retention_curves.png")

def generate_strategy_comparison():
    """生成策略效果对比图"""
    setup_english_fonts()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # 策略对比数据
    strategies = ['Personalized\nRecommendation', 'Popular\nContent', 'Time-based\nPush', 'RFM-based\nTargeting']
    
    # 不同指标的效果对比
    engagement_improvement = [35, 22, 18, 42]  # 参与度提升
    retention_improvement = [28, 15, 12, 38]   # 留存率提升
    revenue_increase = [40, 25, 20, 55]        # 收入增长
    
    x_pos = np.arange(len(strategies))
    width = 0.25
    
    # 绘制柱状图对比
    ax1.bar(x_pos - width, engagement_improvement, width, label='Engagement Improvement', 
            color='#4CAF50', alpha=0.8)
    ax1.bar(x_pos, retention_improvement, width, label='Retention Improvement', 
            color='#2196F3', alpha=0.8)
    ax1.bar(x_pos + width, revenue_increase, width, label='Revenue Increase', 
            color='#FF9800', alpha=0.8)
    
    ax1.set_xlabel('Marketing Strategies', fontsize=12)
    ax1.set_ylabel('Improvement Rate (%)', fontsize=12)
    ax1.set_title('Strategy Effectiveness Comparison', fontsize=14, pad=15)
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(strategies, fontsize=10)
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3, axis='y')
    
    # 绘制策略效果雷达图
    metrics = ['Engagement', 'Retention', 'Revenue', 'Satisfaction', 'Cost Efficiency']
    
    # 不同策略在各指标上的得分
    strategy_scores = {
        'Personalized': [8, 7, 9, 8, 6],
        'Popular': [6, 5, 7, 6, 8],
        'Time-based': [5, 4, 6, 5, 7],
        'RFM-based': [9, 8, 9, 8, 7]
    }
    
    # 雷达图设置
    angles = np.linspace(0, 2*np.pi, len(metrics), endpoint=False).tolist()
    angles += angles[:1]  # 闭合雷达图
    
    colors = ['#4CAF50', '#2196F3', '#FF9800', '#9C27B0']
    
    for i, (strategy, scores) in enumerate(strategy_scores.items()):
        scores += scores[:1]  # 闭合数据
        ax2.plot(angles, scores, 'o-', linewidth=2, label=strategy, color=colors[i])
        ax2.fill(angles, scores, alpha=0.1, color=colors[i])
    
    # 设置雷达图坐标
    ax2.set_xticks(angles[:-1])
    ax2.set_xticklabels(metrics, fontsize=10)
    ax2.set_yticks([2, 4, 6, 8, 10])
    ax2.set_ylim(0, 10)
    ax2.set_title('Strategy Performance Radar Chart', fontsize=14, pad=15)
    ax2.legend(fontsize=10, loc='upper right')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # 保存图表
    os.makedirs('docs/validation', exist_ok=True)
    plt.savefig("docs/validation/strategy_comparison.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ 策略效果对比图已生成: docs/validation/strategy_comparison.png")

if __name__ == "__main__":
    generate_retention_curves()
    generate_strategy_comparison()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
总结与展望类图表生成脚本
图表11: 系统工作流程图
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np
import os

def setup_english_fonts():
    """设置英文字体"""
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['font.size'] = 10

def generate_system_workflow():
    """生成系统工作流程图"""
    setup_english_fonts()
    
    fig, ax = plt.subplots(1, 1, figsize=(18, 10))
    
    # 定义工作流阶段
    stages = [
        {
            "name": "Data Collection", 
            "x": 0.1, "y": 0.8, "color": "lightblue",
            "steps": ["Raw Video Data", "User Behavior Logs", "Program Metadata"]
        },
        {
            "name": "Data Processing", 
            "x": 0.3, "y": 0.8, "color": "lightgreen",
            "steps": ["ETL Pipeline", "Data Cleaning", "Feature Engineering"]
        },
        {
            "name": "RFM Analysis", 
            "x": 0.5, "y": 0.8, "color": "lightyellow",
            "steps": ["Recency Calculation", "Frequency Analysis", "Monetary Value"]
        },
        {
            "name": "User Segmentation", 
            "x": 0.7, "y": 0.8, "color": "lightcoral",
            "steps": ["K-means Clustering", "Segment Profiling", "Behavior Patterns"]
        },
        {
            "name": "Strategy Application", 
            "x": 0.9, "y": 0.8, "color": "lightpink",
            "steps": ["Personalized Push", "Content Recommendation", "Retention Strategy"]
        },
        {
            "name": "Evaluation & Feedback", 
            "x": 0.5, "y": 0.4, "color": "lightgray",
            "steps": ["Effectiveness Metrics", "A/B Testing", "Continuous Optimization"]
        }
    ]
    
    # 绘制各阶段框
    for stage in stages:
        # 阶段主框
        rect = FancyBboxPatch((stage["x"]-0.08, stage["y"]-0.12), 0.16, 0.24,
                             boxstyle="round,pad=0.02", 
                             facecolor=stage["color"], edgecolor="black", linewidth=2)
        ax.add_patch(rect)
        
        # 阶段标题
        ax.text(stage["x"], stage["y"] + 0.08, stage["name"], 
                ha='center', va='center', fontsize=11, weight='bold')
        
        # 步骤列表
        for i, step in enumerate(stage["steps"]):
            ax.text(stage["x"], stage["y"] - 0.02 - i*0.06, step, 
                    ha='center', va='center', fontsize=9)
    
    # 绘制工作流箭头
    arrow_props = dict(arrowstyle="->", color="red", linewidth=2, shrinkA=5, shrinkB=5)
    
    # 水平流程箭头
    ax.annotate('', xy=(0.22, 0.8), xytext=(0.18, 0.8), arrowprops=arrow_props)
    ax.annotate('', xy=(0.42, 0.8), xytext=(0.38, 0.8), arrowprops=arrow_props)
    ax.annotate('', xy=(0.62, 0.8), xytext=(0.58, 0.8), arrowprops=arrow_props)
    ax.annotate('', xy=(0.82, 0.8), xytext=(0.78, 0.8), arrowprops=arrow_props)
    
    # 垂直反馈箭头
    ax.annotate('', xy=(0.5, 0.52), xytext=(0.5, 0.48), arrowprops=arrow_props)
    
    # 从策略应用到评估的反馈箭头
    ax.annotate('', xy=(0.7, 0.6), xytext=(0.6, 0.45), 
                arrowprops=dict(arrowstyle="->", color="blue", linewidth=2, 
                              connectionstyle="arc3,rad=-0.2"))
    
    # 从评估到数据处理的优化箭头
    ax.annotate('', xy=(0.4, 0.45), xytext=(0.3, 0.6), 
                arrowprops=dict(arrowstyle="->", color="green", linewidth=2, 
                              connectionstyle="arc3,rad=0.2"))
    
    # 添加流程标签
    ax.text(0.2, 0.85, 'Data Flow →', fontsize=10, color='red', weight='bold')
    ax.text(0.4, 0.85, 'Processing →', fontsize=10, color='red', weight='bold')
    ax.text(0.6, 0.85, 'Analysis →', fontsize=10, color='red', weight='bold')
    ax.text(0.8, 0.85, 'Segmentation →', fontsize=10, color='red', weight='bold')
    
    ax.text(0.52, 0.46, 'Evaluation ↓', fontsize=10, color='red', weight='bold')
    ax.text(0.65, 0.55, 'Feedback →', fontsize=10, color='blue', weight='bold')
    ax.text(0.35, 0.55, 'Optimization →', fontsize=10, color='green', weight='bold')
    
    # 添加系统边界
    boundary_rect = patches.Rectangle((0.05, 0.35), 0.9, 0.6, 
                                    linewidth=3, edgecolor='black', 
                                    facecolor='none', linestyle='--', alpha=0.5)
    ax.add_patch(boundary_rect)
    
    ax.text(0.5, 0.3, 'RFM Analysis System Boundary', 
            ha='center', va='center', fontsize=12, weight='bold', 
            bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.9))
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    plt.title("Video Platform RFM Analysis System Workflow", fontsize=16, pad=20)
    
    # 保存图表
    os.makedirs('docs/summary', exist_ok=True)
    plt.savefig("docs/summary/system_workflow.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ 系统工作流程图已生成: docs/summary/system_workflow.png")

def generate_future_roadmap():
    """生成技术发展路线图（额外图表）"""
    setup_english_fonts()
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 8))
    
    # 定义发展路线
    roadmap = [
        {
            "phase": "Phase 1 (Current)",
            "timeline": "2024",
            "milestones": ["Basic RFM Analysis", "User Segmentation", "Manual Strategy"],
            "color": "lightgreen"
        },
        {
            "phase": "Phase 2 (Next 1-2 Years)",
            "timeline": "2025-2026",
            "milestones": ["Real-time Analysis", "AI Recommendations", "Automated Optimization"],
            "color": "lightblue"
        },
        {
            "phase": "Phase 3 (Future)",
            "timeline": "2027+",
            "milestones": ["Predictive Analytics", "Cross-platform Integration", "Advanced AI Models"],
            "color": "lightcoral"
        }
    ]
    
    # 绘制路线图
    for i, phase in enumerate(roadmap):
        x_pos = 0.2 + i * 0.3
        
        # 阶段框
        rect = FancyBboxPatch((x_pos-0.12, 0.6), 0.24, 0.3,
                             boxstyle="round,pad=0.02", 
                             facecolor=phase["color"], edgecolor="black", linewidth=2)
        ax.add_patch(rect)
        
        # 阶段标题
        ax.text(x_pos, 0.85, phase["phase"], 
                ha='center', va='center', fontsize=12, weight='bold')
        
        # 时间线
        ax.text(x_pos, 0.78, phase["timeline"], 
                ha='center', va='center', fontsize=10, style='italic')
        
        # 里程碑
        for j, milestone in enumerate(phase["milestones"]):
            ax.text(x_pos, 0.7 - j*0.08, f"• {milestone}", 
                    ha='center', va='center', fontsize=9)
        
        # 连接箭头（除了最后一个阶段）
        if i < len(roadmap) - 1:
            ax.annotate('', xy=(x_pos+0.15, 0.75), xytext=(x_pos+0.27, 0.75), 
                       arrowprops=dict(arrowstyle="->", color="red", linewidth=2))
    
    # 添加标题和说明
    ax.text(0.5, 0.95, "Technology Development Roadmap", 
            ha='center', va='center', fontsize=16, weight='bold')
    
    ax.text(0.5, 0.4, "Future Directions: Integration with advanced AI technologies, real-time processing capabilities, \nand cross-platform user behavior analysis for comprehensive customer insights.", 
            ha='center', va='center', fontsize=11, 
            bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.7))
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    # 保存图表
    os.makedirs('docs/summary', exist_ok=True)
    plt.savefig("docs/summary/future_roadmap.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ 技术发展路线图已生成: docs/summary/future_roadmap.png")

if __name__ == "__main__":
    generate_system_workflow()
    generate_future_roadmap()

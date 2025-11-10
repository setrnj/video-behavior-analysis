#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统架构与设计类图表生成脚本
图表1: 系统整体架构图
图表2: 数据仓库星型模型ER图
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

def generate_system_architecture():
    """生成系统整体架构图"""
    setup_english_fonts()
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    
    # 定义各层位置和大小
    layers = [
        {"name": "Data Storage Layer", "components": ["HDFS", "Hive", "MySQL"], 
         "y": 0.1, "color": "lightblue", "height": 0.2},
        {"name": "Processing Layer", "components": ["ETL Module", "RFM Calculation", "Clustering Analysis"], 
         "y": 0.4, "color": "lightgreen", "height": 0.2},
        {"name": "Application Layer", "components": ["Visualization Module", "Report Generation"], 
         "y": 0.7, "color": "lightyellow", "height": 0.2}
    ]
    
    # 绘制各层
    for i, layer in enumerate(layers):
        # 绘制层框
        rect = FancyBboxPatch((0.1, layer["y"]), 0.8, layer["height"], 
                             boxstyle="round,pad=0.02", 
                             facecolor=layer["color"], edgecolor="black", linewidth=2)
        ax.add_patch(rect)
        
        # 层标题
        ax.text(0.5, layer["y"] + layer["height"] - 0.05, layer["name"], 
                ha='center', va='center', fontsize=14, weight='bold')
        
        # 组件
        for j, comp in enumerate(layer["components"]):
            ax.text(0.5, layer["y"] + layer["height"] - 0.1 - j*0.06, comp, 
                    ha='center', va='center', fontsize=11, bbox=dict(boxstyle="round,pad=0.3", 
                    facecolor="white", alpha=0.8))
    
    # 绘制数据流箭头
    arrow_props = dict(arrowstyle="->", color="red", linewidth=2)
    
    # 数据流方向
    ax.annotate('', xy=(0.5, 0.3), xytext=(0.5, 0.25), 
                arrowprops=arrow_props)
    ax.annotate('', xy=(0.5, 0.6), xytext=(0.5, 0.55), 
                arrowprops=arrow_props)
    
    # 添加数据流标签
    ax.text(0.55, 0.275, 'Raw Data →', fontsize=10, color='red')
    ax.text(0.55, 0.575, 'Processed Data →', fontsize=10, color='red')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    plt.title("Video Platform RFM Analysis System Architecture", fontsize=16, pad=20)
    
    # 保存图表
    os.makedirs('docs/system', exist_ok=True)
    plt.savefig("docs/system/system_architecture.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ 系统架构图已生成: docs/system/system_architecture.png")

def generate_er_diagram():
    """生成数据仓库星型模型ER图"""
    setup_english_fonts()
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    
    # 定义实体位置和属性
    entities = {
        "fact_watching": {
            "x": 0.5, "y": 0.5, "color": "lightcoral", 
            "fields": ["user_id", "program_id", "time_id", "watch_duration", "watch_count"]
        },
        "dim_user": {
            "x": 0.2, "y": 0.8, "color": "lightblue", 
            "fields": ["user_id", "age", "gender", "region", "register_date"]
        },
        "dim_time": {
            "x": 0.8, "y": 0.8, "color": "lightgreen", 
            "fields": ["time_id", "date", "hour", "weekday", "month"]
        },
        "dim_program": {
            "x": 0.2, "y": 0.2, "color": "lightyellow", 
            "fields": ["program_id", "category", "duration", "producer", "release_date"]
        },
        "dim_channel": {
            "x": 0.8, "y": 0.2, "color": "lightpink", 
            "fields": ["channel_id", "channel_name", "category", "subscribers"]
        }
    }
    
    # 绘制实体框
    for name, entity in entities.items():
        # 实体框
        rect = FancyBboxPatch((entity["x"]-0.15, entity["y"]-0.12), 0.3, 0.24,
                             boxstyle="round,pad=0.02", 
                             facecolor=entity["color"], edgecolor="black", linewidth=2)
        ax.add_patch(rect)
        
        # 实体名称
        ax.text(entity["x"], entity["y"] + 0.08, name.replace('_', ' ').title(), 
                ha='center', va='center', fontsize=12, weight='bold')
        
        # 字段列表
        for i, field in enumerate(entity["fields"]):
            ax.text(entity["x"], entity["y"] - 0.02 - i*0.04, field, 
                    ha='center', va='center', fontsize=9)
    
    # 绘制关联关系线
    for dim_name in ["dim_user", "dim_time", "dim_program", "dim_channel"]:
        dim_entity = entities[dim_name]
        fact_entity = entities["fact_watching"]
        
        # 计算连线方向
        dx = fact_entity["x"] - dim_entity["x"]
        dy = fact_entity["y"] - dim_entity["y"]
        
        # 绘制连线
        ax.plot([dim_entity["x"], fact_entity["x"]], 
                [dim_entity["y"], fact_entity["y"]], 
                'k-', linewidth=1, alpha=0.7)
        
        # 添加关系标注
        mid_x = (dim_entity["x"] + fact_entity["x"]) / 2
        mid_y = (dim_entity["y"] + fact_entity["y"]) / 2
        ax.text(mid_x, mid_y, '1:N', fontsize=8, 
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8))
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    plt.title("Data Warehouse Star Schema ER Diagram", fontsize=16, pad=20)
    
    # 添加图例说明
    ax.text(0.02, 0.02, "● Fact Table (中心表)\n● Dimension Tables (维度表)\n● 1:N Relationships (一对多关系)", 
            fontsize=10, bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.9))
    
    # 保存图表
    os.makedirs('docs/system', exist_ok=True)
    plt.savefig("docs/system/er_diagram.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ ER图已生成: docs/system/er_diagram.png")

if __name__ == "__main__":
    generate_system_architecture()
    generate_er_diagram()

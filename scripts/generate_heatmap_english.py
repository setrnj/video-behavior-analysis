#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

def generate_hourly_heatmap():
    # 使用默认英文字体，移除中文字体设置
    
    try:
        # 从 HDFS 获取预处理数据
        import subprocess
        subprocess.run(["hdfs", "dfs", "-get", "/results/time_heatmap/000000_0", "time_heatmap.csv"])
        df = pd.read_csv('time_heatmap.csv', 
                         names=['hour_of_day', 'day_of_week', 'sessions', 'avg_duration'])
        
        # 重命名列
        df = df.rename(columns={'sessions': 'active_users'})
        print("Successfully loaded data from HDFS")
    except Exception as e:
        print(f"Data loading failed: {str(e)}")
        print("Using sample data to generate heatmap...")
        # 创建示例数据
        data = {
            'hour_of_day': list(range(0, 24)) * 7,
            'day_of_week': [d for d in range(1, 8) for _ in range(24)],
            'active_users': [max(50, (h*10) % 200) for h in range(24*7)]
        }
        df = pd.DataFrame(data)
    
    # 确保目录存在
    os.makedirs("docs", exist_ok=True)
    
    # 转换星期几为英文标签
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    df['day_of_week'] = df['day_of_week'].apply(lambda x: weekdays[x-1] if 1 <= x <= 7 else "Invalid")
    
    # 创建热力图矩阵
    heatmap_data = df.pivot_table(index="hour_of_day", 
                                 columns="day_of_week", 
                                 values="active_users", 
                                 fill_value=0)
    
    # 生成热力图
    plt.figure(figsize=(12, 8))
    plt.imshow(heatmap_data, cmap="YlGnBu", aspect='auto')
    plt.colorbar(label='Active Users')
    
    # 设置坐标轴
    plt.yticks(range(len(heatmap_data.index)), heatmap_data.index)
    plt.xticks(range(len(heatmap_data.columns)), heatmap_data.columns, rotation=45)
    
    plt.title("User Activity Heatmap by Hour and Day")
    plt.xlabel("Day of Week")
    plt.ylabel("Hour of Day")
    plt.tight_layout()
    
    plt.savefig("docs/hourly_heatmap_english.png", dpi=150, bbox_inches='tight')
    print("Heatmap generated: docs/hourly_heatmap_english.png")
    
if __name__ == "__main__":
    generate_hourly_heatmap()

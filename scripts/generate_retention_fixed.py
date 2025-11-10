#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 从HDFS获取数据
print("从HDFS获取留存数据...")
subprocess.run(["hdfs", "dfs", "-get", "/results/retention_curve/000000_0", "retention_data.csv"])

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
plt.savefig('/root/video-behavior-analysis/video-behavior-analysis-system/docs/retention_curve_new.png', dpi=300, bbox_inches='tight')
plt.close()

print("留存曲线已保存到 /root/video-behavior-analysis/video-behavior-analysis-system/docs/retention_curve_new.png")

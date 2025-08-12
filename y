#!/bin/bash

# 1. 执行SQL分析
hive -f sql_scripts/05_top_analysis.hql
hive -f sql_scripts/06_user_behavior.hql

# 2. 生成可视化文档
python scripts/generate_segmentation.py
python scripts/generate_heatmap.py
python scripts/generate_retention.py

# 3. 整合到README
echo "![用户分群模型](docs/user_segmentation.png)" >> README.md
echo "![时段热力图](docs/hourly_heatmap.png)" >> README.md
echo "![留存曲线](docs/retention_curve.png)" >> README.md

echo "可视化文档生成完成!"

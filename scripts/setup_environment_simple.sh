#!/bin/bash
echo "=== 环境初始化 ==="

# 创建必要目录
mkdir -p logs
mkdir -p data/{raw,processed,results}
mkdir -p outputs/{charts,reports}

# 安装Python依赖
echo "安装Python依赖..."
pip3 install --user pandas matplotlib seaborn scikit-learn pyhive thrift fpdf

# 创建HDFS目录
echo "创建HDFS目录..."
hdfs dfs -mkdir -p /data/video_analysis/{raw/{media,users},cleaned,dwh,results}
hdfs dfs -mkdir -p /results/{user_rfm,time_heatmap,retention_curve}
hdfs dfs -chmod -R 755 /data/video_analysis
hdfs dfs -chmod -R 755 /results

# 创建Hive数据库
echo "创建Hive数据库..."
hive -e "CREATE DATABASE IF NOT EXISTS video_analysis;"

echo "环境初始化完成！"

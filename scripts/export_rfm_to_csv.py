#!/usr/bin/env python3
"""
从 Hive 导出 RFM 数据到本地 CSV 文件
"""

import os
from pyhive import hive
import pandas as pd

# --- 配置 ---
HIVE_HOST = 'localhost'  # 根据你的 HiveServer2 地址修改
HIVE_PORT = 10000
HIVE_DATABASE = 'video_analysis'
OUTPUT_CSV_PATH = '../results/rfm_data_for_clustering.csv'

def export_rfm():
    print("开始连接 Hive...")
    conn = hive.Connection(host=HIVE_HOST, port=HIVE_PORT, database=HIVE_DATABASE)
    
    query = """
        SELECT 
            user_key,
            recency,
            frequency,
            monetary
        FROM dws.r_user_rfm
    """
    
    print(f"正在执行查询: {query}")
    df = pd.read_sql(query, conn)
    print(f"查询完成，共获取 {len(df)} 条记录.")
    
    print(f"保存到 CSV: {OUTPUT_CSV_PATH}")
    df.to_csv(OUTPUT_CSV_PATH, index=False)
    print("导出完成.")

if __name__ == "__main__":
    export_rfm()

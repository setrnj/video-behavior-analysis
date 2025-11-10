#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的视频平台RFM分析系统主程序
"""

import os
import sys
import subprocess
import argparse

def run_command(cmd, description):
    """运行命令并显示结果"""
    print(f"\n=== {description} ===")
    print(f"执行命令: {cmd}")
    try:
        # 使用Python 3.6兼容的方式
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            print("✅ 执行成功")
            if result.stdout:
                print("输出:", result.stdout)
        else:
            print("❌ 执行失败")
            print("错误:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ 执行异常: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='视频平台RFM分析系统')
    parser.add_argument('--mode', choices=['etl', 'rfm', 'viz', 'all'], 
                       default='all', help='运行模式')
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("视频平台RFM分析系统")
    print("=" * 50)
    
    success = True
    
    if args.mode in ['etl', 'all']:
        # ETL流程
        success &= run_command("hive -f ../sql_scripts/01_ddl_table_creation.hql", "创建表结构")
        success &= run_command("hive -f ../sql_scripts/02_data_cleaning.hql", "数据清洗")
        success &= run_command("hive -f ../sql_scripts/03_dimension_loading.hql", "维度加载")
        success &= run_command("hive -f ../sql_scripts/04_fact_loading.hql", "事实表加载")
    
    if args.mode in ['rfm', 'all']:
        # RFM分析
        success &= run_command("hive -f ../sql_scripts/05_top_analysis.hql", "RFM分析")
        success &= run_command("hive -f ../sql_scripts/06_user_behavior.hql", "用户行为分析")
        success &= run_command("hive -f ../sql_scripts/07_user_retention.hql", "留存分析")
    
    if args.mode in ['viz', 'all']:
        # 可视化
        success &= run_command("python3 ../scripts/generate_heatmap.py", "生成热力图")
        success &= run_command("python3 ../scripts/generate_retention.py", "生成留存曲线")
        success &= run_command("python3 ../scripts/generate_segmentation.py", "生成用户分群")
    
    if success:
        print("\n🎉 所有任务执行完成！")
    else:
        print("\n⚠️ 部分任务执行失败，请检查日志")
        sys.exit(1)

if __name__ == "__main__":
    main()

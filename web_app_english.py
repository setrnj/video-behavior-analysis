#!/usr/bin/env python3
from flask import Flask, render_template, send_file, jsonify
import os
import json

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Video Behavior Analysis System</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .header { background: #f0f0f0; padding: 20px; border-radius: 5px; }
            .nav { margin: 20px 0; }
            .nav a { display: inline-block; margin-right: 15px; padding: 10px 20px; 
                    background: #007cba; color: white; text-decoration: none; border-radius: 3px; }
            .nav a:hover { background: #005a87; }
            .chart-container { margin: 20px 0; padding: 20px; border: 1px solid #ddd; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Video Behavior Analysis System</h1>
            <p>User Behavior Analysis Platform based on RFM Model</p>
        </div>
        
        <div class="nav">
            <a href="/segment-analysis">User Segmentation Analysis</a>
            <a href="/data-management">Data Management</a>
        </div>
        
        <div class="content">
            <h2>System Features</h2>
            <ul>
                <li>User behavior data ETL processing</li>
                <li>RFM user segmentation analysis</li>
                <li>User retention analysis</li>
                <li>Data visualization</li>
            </ul>
            
            <h2>Recently Generated Charts</h2>
            <div class="chart-container">
                <h3>User Segmentation</h3>
                <img src="/api/charts/user_segmentation_english.png" width="800" alt="User Segmentation Chart">
            </div>
            
            <div class="chart-container">
                <h3>Hourly Heatmap</h3>
                <img src="/api/charts/hourly_heatmap_english.png" width="800" alt="Hourly Heatmap">
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/segment-analysis')
def segment_analysis():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>User Segmentation Analysis - Video Behavior Analysis System</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .nav { margin: 20px 0; }
            .nav a { display: inline-block; margin-right: 15px; padding: 10px 20px; 
                    background: #007cba; color: white; text-decoration: none; border-radius: 3px; }
            .chart-container { margin: 20px 0; padding: 20px; border: 1px solid #ddd; }
        </style>
    </head>
    <body>
        <div class="nav">
            <a href="/">Home</a>
            <a href="/segment-analysis">User Segmentation</a>
            <a href="/data-management">Data Management</a>
        </div>
        
        <h1>User Segmentation Analysis</h1>
        
        <div class="chart-container">
            <h3>RFM User Segmentation</h3>
            <img src="/api/charts/user_segmentation_english.png" width="800" alt="User Segmentation Chart">
        </div>
        
        <div class="chart-container">
            <h3>User Retention Curve</h3>
            <img src="/api/charts/retention_curve_english.png" width="800" alt="Retention Curve">
        </div>
        
        <div class="chart-container">
            <h3>RFM Distribution</h3>
            <img src="/api/charts/rfm_distribution_english.png" width="800" alt="RFM Distribution">
        </div>
    </body>
    </html>
    '''

@app.route('/data-management')
def data_management():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Data Management - Video Behavior Analysis System</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .nav { margin: 20px 0; }
            .nav a { display: inline-block; margin-right: 15px; padding: 10px 20px; 
                    background: #007cba; color: white; text-decoration: none; border-radius: 3px; }
            .content { margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="nav">
            <a href="/">Home</a>
            <a href="/segment-analysis">User Segmentation</a>
            <a href="/data-management">Data Management</a>
        </div>
        
        <h1>Data Management</h1>
        
        <div class="content">
            <h2>Data Processing Status</h2>
            <p>Data management features are under development.</p>
            
            <h2>Available Data Sources</h2>
            <ul>
                <li>User behavior logs</li>
                <li>Video interaction data</li>
                <li>Session analytics</li>
                <li>RFM analysis results</li>
            </ul>
        </div>
    </body>
    </html>
    '''

@app.route('/api/charts/<chart_name>')
def get_chart(chart_name):
    """Get chart files"""
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    chart_paths = [
        f"docs/{chart_name}",
        f"scripts/docs/{chart_name}",
        f"scripts/outputs/{chart_name}",
        f"outputs/{chart_name}",
        f"results/{chart_name}"
    ]

    for path in chart_paths:
        if os.path.exists(path):
            logger.info(f"Found chart at: {path}")
            return send_file(path)

    logger.error(f"Chart {chart_name} not found in any of the following paths: {chart_paths}")
    return f"Chart {chart_name} not found", 404
@app.route('/api/analysis-results')
def get_analysis_results():
    """Get analysis results data"""
    try:
        results = {
            "user_segments": [
                {"segment": "High Value Users", "count": 1500, "percentage": 15},
                {"segment": "Medium Value Users", "count": 4500, "percentage": 45},
                {"segment": "Low Value Users", "count": 4000, "percentage": 40}
            ],
            "total_users": 10000
        }
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)


import pandas as pd
import os
from sklearn.cluster import KMeans
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_CSV = os.path.join(BASE_DIR, "results", "rfm_data_for_clustering.csv")
OUTPUT_CSV = os.path.join(BASE_DIR, "results", "rfm_kmeans_clusters.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "kmeans_model.pkl")

def perform_kmeans():
    print("读取 RFM 数据（无表头）...")
    # 因为没有 header，需手动指定列名或直接按位置取
    df = pd.read_csv(INPUT_CSV, header=None)
    print(f"数据形状: {df.shape}")  # 应该是 (N, 8)

    # 方案A：使用原始 RFM 值（第1~3列，即索引1,2,3）
    # rfm_cols = ['recency', 'frequency', 'monetary']
    # X = df.iloc[:, 1:4]

    # 方案B（推荐）：使用 RFM 得分（第4~6列，即索引4,5,6）
    X = df.iloc[:, 4:7]
    print("使用列（R_score, F_score, M_score）进行聚类...")

    print("训练 K-Means 模型...")
    kmeans = KMeans(n_clusters=4, random_state=42)
    df['cluster'] = kmeans.fit_predict(X)

    # 保存结果（保留所有原始列 + cluster）
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    df.to_csv(OUTPUT_CSV, index=False, header=False)  # 保持无 header 风格

    # 保存模型
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(kmeans, MODEL_PATH)

    print(f"✅ 聚类完成！结果已保存到: {OUTPUT_CSV}")
    print("各簇中心:")
    print(kmeans.cluster_centers_)

if __name__ == "__main__":
    perform_kmeans()

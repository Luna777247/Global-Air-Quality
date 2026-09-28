# Global Air Quality — Pollution Fingerprint

## Mục tiêu

Project tập trung vào một bài toán duy nhất:

> **Mỗi thành phố có kiểu ô nhiễm đặc trưng như thế nào, và những thành phố nào có profile ô nhiễm tương đồng?**

Phân tích sử dụng 6 pollutant:

- PM2.5
- PM10
- NO2
- SO2
- O3
- CO

## Methodology

```text
Raw air-quality data
        ↓
City pollution profile
        ↓
StandardScaler
        ↓
K-Means clustering
        ↓
Pollution fingerprint
        ↓
Cosine similarity
        ↓
Global cluster map
```

## Kết quả hiện tại

- Số city: 50
- Số country: 38
- Số cluster được chọn: 6
- Silhouette score tốt nhất: 0.1945

### Silhouette scores

- k=2: 0.1696
- k=3: 0.1795
- k=4: 0.1677
- k=5: 0.1921
- k=6: 0.1945
- k=7: 0.1726
- k=8: 0.1768

## Các file chính

- `data/processed/city_pollution_profile.csv`: mean pollutant profile theo city.
- `data/processed/city_fingerprint.csv`: standardized fingerprint + cluster.
- `data/processed/city_similarity.csv`: cosine similarity giữa các city.
- `outputs/cluster_summary.csv`: đặc điểm của từng cluster.
- `outputs/city_cluster.csv`: city + country + coordinates + cluster.
- `models/pollution_cluster.pkl`: pipeline scaler + K-Means.
- `analysis/pollution_fingerprint.ipynb`: notebook tái hiện phân tích.
- `app/app.py`: Streamlit explorer.

## Chạy project

```bash
pip install -r requirements.txt
streamlit run app/app.py
```

## Lưu ý

Cluster profile là kết quả unsupervised learning. Các tên như "PM2.5 dominant" chỉ nên được xem là **diễn giải hậu nghiệm** dựa trên standardized cluster means, không phải nhãn được biết trước.

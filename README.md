# NLP VNExpress News Classification Project

Dự án phân loại tin tức tiếng Việt từ nguồn VNExpress sử dụng mô hình Naive Bayes. Dự án được thực hiện để tự động phân loại các bài báo vào các chuyên mục như Kinh doanh, Thể thao, Sức khỏe, Thời sự, Giải trí, Du lịch, Pháp luật.

## 1. Yêu cầu hệ thống
- Python 3.11+
- Các thư viện liệt kê trong `requirements.txt`

## 2. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

## 3. Chạy hệ thống

### Bước 1: Thu thập dữ liệu
Chạy script `scraper.py` để lấy dữ liệu từ RSS feeds của VNExpress. Dữ liệu sau thu thập và tiền xử lý sẽ được lưu vào file `news_dataset.csv`.
```bash
python scraper.py
```

### Bước 2: Huấn luyện mô hình Naive Bayes
Sử dụng script `train.py` để tiền xử lý văn bản, trích xuất đặc trưng với TF-IDF và huấn luyện mô hình phân loại (MultinomialNB).
```bash
python train.py
```
Mô hình sẽ sinh ra hai file: `naive_bayes_model.pkl` và `tfidf_vectorizer.pkl`.

### Bước 3: Deploy/Chạy Web Interface
Sử dụng Streamlit để khởi chạy giao diện kiểm thử.
```bash
streamlit run app.py
```
Sau đó truy cập đường link localhost `http://localhost:8501` để dán một URL bài báo từ VNExpress và kiểm tra dự đoán.

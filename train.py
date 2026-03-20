import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

def main():
    print("Đang đọc dữ liệu...")
    try:
        df = pd.read_csv('news_dataset.csv')
    except Exception as e:
        print(f"Lỗi đọc dữ liệu: {e}")
        return

    df = df.dropna(subset=['content_cleaned', 'label'])
    X = df['content_cleaned']
    y = df['label']
    
    print("Chia tập dữ liệu...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Vector hóa văn bản...")
    vectorizer = TfidfVectorizer(max_features=5000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    print("Huấn luyện mô hình Naive Bayes...")
    model = MultinomialNB()
    model.fit(X_train_vec, y_train)
    
    print("Đánh giá mô hình...")
    y_pred = model.predict(X_test_vec)
    acc = accuracy_score(y_test, y_pred)
    print(f"Độ chính xác: {acc*100:.2f}%")
    print("\nChi tiết Classification Report:\n")
    print(classification_report(y_test, y_pred, zero_division=0))
    
    print("Lưu mô hình...")
    joblib.dump(model, 'naive_bayes_model.pkl')
    joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')
    print("Hoàn tất! Mô hình đã lưu tại naive_bayes_model.pkl")

if __name__ == '__main__':
    main()

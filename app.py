import streamlit as st
import joblib
import pandas as pd
from scraper import get_article_content, clean_text

st.set_page_config(page_title="VNExpress News Classifier", page_icon="📰", layout="wide")

@st.cache_resource
def load_models():
    model = joblib.load('naive_bayes_model.pkl')
    vectorizer = joblib.load('tfidf_vectorizer.pkl')
    return model, vectorizer

st.title("Phân Loại Tin Tức VNExpress 📰")
st.write("Dự án NLP - Phân loại thể loại bài báo sử dụng mô hình Naive Bayes.")

try:
    model, vectorizer = load_models()
except:
    st.error("Chưa tìm thấy mô hình. Vui lòng chạy `python train.py` trước.")
    st.stop()

url = st.text_input("Nhập đường dẫn bài báo VNExpress:")
if st.button("Phân Loại"):
    if url:
        with st.spinner("Đang lấy nội dung bài báo..."):
            content = get_article_content(url)
            if not content:
                st.error("Không thể lấy nội dung bài báo. Vui lòng kiểm tra lại URL.")
            else:
                st.write("**Nội dung gốc (một phần):**")
                st.info(content[:300] + "...")
                
                with st.spinner("Đang phân tích và dự đoán..."):
                    cleaned = clean_text(content)
                    if not cleaned:
                        st.error("Nội dung quá ngắn hoặc không hợp lệ để phân loại.")
                    else:
                        X_vec = vectorizer.transform([cleaned])
                        prediction = model.predict(X_vec)[0]
                        st.success(f"Dự đoán Thể loại: **{prediction}**")
                        
                        proba = model.predict_proba(X_vec)[0]
                        classes = model.classes_
                        st.write("Xác suất dự đoán:")
                        for c, p in zip(classes, proba):
                            st.write(f"- {c}: {p*100:.2f}%")
    else:
        st.warning("Vui lòng nhập URL.")

import feedparser
import pandas as pd
import time
import requests
from bs4 import BeautifulSoup
from underthesea import word_tokenize
import re

RSS_FEEDS = {
    'Kinh doanh': 'https://vnexpress.net/rss/kinh-doanh.rss',
    'The thao': 'https://vnexpress.net/rss/the-thao.rss',
    'Suc khoe': 'https://vnexpress.net/rss/suc-khoe.rss',
    'Thoi su': 'https://vnexpress.net/rss/thoi-su.rss',
    'Giai tri': 'https://vnexpress.net/rss/giai-tri.rss',
    'Du lich': 'https://vnexpress.net/rss/du-lich.rss',
    'Pháp luật': 'https://vnexpress.net/rss/phap-luat.rss',
    'Giáo dục': 'https://vnexpress.net/rss/giao-duc.rss',
    'Khoa học': 'https://vnexpress.net/rss/khoa-hoc.rss',
    'Xe': 'https://vnexpress.net/rss/oto-xe-may.rss',
    'Thế giới': 'https://vnexpress.net/rss/the-gioi.rss',
    'Số hóa': 'https://vnexpress.net/rss/so-hoa.rss',
    'Đời sống': 'https://vnexpress.net/rss/gia-dinh.rss'
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)',
}

STOPWORDS = set([
    'và', 'hoặc', 'nhưng', 'vì', 'nếu', 'thì', 'hay',
    'là', 'được', 'có', 'của', 'cho', 'để', 'trong', 'với',
    'từ', 'bởi', 'về', 'đã', 'sẽ', 'đang', 'các', 'những',
    'này', 'đó', 'kia', 'nào', 'ai', 'gì', 'đâu', 'sao',
    'như', 'theo', 'trên', 'dưới', 'giữa', 'ngoài', 'sau', 'trước',
    'một', 'những', 'các', 'cái', 'việc', 'khi', 'lúc', 'đến', 'ra', 'vào', 'phải'
])

def get_article_content(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.encoding = 'utf-8'
        if response.status_code != 200: return None
        soup = BeautifulSoup(response.content, 'html.parser')
        content_div = soup.find('article', class_='fck_detail') or soup.find('div', class_='fck_detail')
        if not content_div: return None
        paragraphs = content_div.find_all('p', class_='Normal') or content_div.find_all('p')
        content = ' '.join([p.get_text().strip() for p in paragraphs])
        return content
    except Exception:
        return None

def clean_text(text):
    if not text or len(text) < 100: return None
    text = text.lower()
    text = re.sub(r'[^a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    try:
        tokens = word_tokenize(text, format="text")
    except:
        tokens = text
    words = tokens.split()
    filtered_words = [word for word in words if word not in STOPWORDS and len(word) > 1]
    return ' '.join(filtered_words)

def main():
    data = []
    print("Đang thu thập dữ liệu từ VNExpress RSS...")
    for label, rss_url in RSS_FEEDS.items():
        print(f"Đang thu thập chuyên mục: {label}")
        try:
            feed = feedparser.parse(rss_url)
            count = 0
            for entry in feed.entries:  # Lấy toàn bộ bài viết có trong RSS
                title = entry.title if hasattr(entry, 'title') else None
                link = entry.link if hasattr(entry, 'link') else None
                if not title or not link: continue
                content = get_article_content(link)
                if not content or len(content) < 100: continue
                cleaned = clean_text(content)
                if cleaned:
                    data.append({
                        'title': title,
                        'content': content,
                        'content_cleaned': cleaned,
                        'label': label,
                        'url': link
                    })
                    count += 1
                time.sleep(0.5)
            print(f"--> Thu thập thành công {count} bài viết của {label}")
        except Exception as e:
            print(f"Lỗi khi thu thập {label}: {e}")
            
    df = pd.DataFrame(data)
    df.to_csv('news_dataset.csv', index=False, encoding='utf-8-sig')
    print("HOÀN THÀNH. Dữ liệu được lưu tại news_dataset.csv")

if __name__ == '__main__':
    main()

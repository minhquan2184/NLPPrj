# Vietnamese News Classification Project

An NLP project designed to automatically classify Vietnamese news articles from **VNExpress** into categories such as Business, Sports, Health, etc., using a **Naive Bayes** model.

## Project Overview
The system consists of:
1.  **Web Scraper**: Collects data from RSS feeds of various VNExpress categories.
2.  **Model Training Pipeline**: Preprocesses text (using `underthesea` for Vietnamese tokenization), extracts features (`TfidfVectorizer`), and trains a `MultinomialNB` classifier.
3.  **Web Interface**: A Streamlit dashboard to predict the category of an article given its URL in real-time.

---

## Deployment & Installation

### Prerequisites
- Python 3.11 or higher
- Internet connection (for scraping)

### Setup
1.  **Clone the repository** (if applicable) or navigate to the project folder.
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

---

## Data Management

### Downloading/Generating Data
Data is collected by scraping VNExpress RSS feeds.

To generate the dataset (`news_dataset.csv`):
```bash
python scraper.py
```
*   **What it does**: Fetches articles, extracts content, cleans text (removes stopwords, tokenizes), and saves a CSV file containing: `title`, `content`, `content_cleaned`, `label`, `url`.
*   *Note*: A pre-collected `news_dataset.csv` is usually included in this workspace.

---

## Model Training & Management

### Training the Model
To train the classifier on the dataset:
```bash
python train.py
```
*   **What it does**: Splits data into train/test sets, fits a `TfidfVectorizer` (saves as `tfidf_vectorizer.pkl`), trains a `MultinomialNB` model (saves as `naive_bayes_model.pkl`), and prints a performance report.

### Model Artifacts
The training procedure outputs:
-   `naive_bayes_model.pkl`: The trained classifier.
-   `tfidf_vectorizer.pkl`: The fitted text vectorizer.

---

## Running the Application

Launch the Streamlit interface to test the model:
```bash
streamlit run app.py
```
1.  Open the displayed URL (usually `http://localhost:8501`).
2.  Paste a VNExpress article URL into the input field.
3.  Click **Phân Loại** to see the predicted category and class probabilities.

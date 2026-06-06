# iBrand

iBrand is a smart content generation platform that helps brands and social media marketers catch trends early and generate catchy, engaging posts in their own brand voice. It does this by scraping trending news, enriching the data, and streaming it through a big data pipeline where personalized social media content is generated using AI and NLP.

---

## 🚀 Project Structure

```
iBrand/
├── backend/
│   ├── app/
│   │   ├── emoji_api.py           
│   │   ├── index.py               
│   │   └── .dockerignore          
│
├── frontend/
│   └── index.js                  
│
├── news-pipeline/
│   ├── enrichment/
│   │   ├── models/                
│   │   │   (filenames not shown) 
│   │   ├── download_models.py     
│   │   ├── enrich_articles.py     
│   │   └── requirements.txt       
│   │
│   ├── kafka_app/                 
│
│   ├── scrapers/                  
│
│   ├── seed/                      
│
│   ├── spark/                    
│
│   └── .dockerignore             

│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
```

---

## 🧠 How It Works (Pipeline Overview)

The `news-pipeline/` ingests and processes real-time news using the following stack:
**Scrapers** : Collect trending news articles from multiple sources in near real-time.
**Kafka Producers**: Multiple producer scripts publish raw news data to Kafka topic news-articles.
**Spark Streaming Jobs**: Consume the Kafka topic, perform real-time processing including:
Parsing and cleaning the raw news data.
- Applying enrichment like Named Entity Recognition (NER), sentiment analysis, or topic tagging.
- Summarization using HuggingFace transformer models.
- Embedding sentences with Sentence-Transformers for semantic analysis.
**AI/NLP Models**:
Sentence embedding models (e.g., all-MiniLM-L6-v2) for semantic similarity and clustering.
DistilBERT for masked language modeling and feature extraction.
BART-large-MNLI for zero-shot classification (topic categorization or sentiment inference).
Summarization models for concise content generation.
**MongoDB Atlas** : Enriched, summarized, and structured news articles are stored for downstream use.
**Docker Compose**: Manages all services including Kafka, Spark, MongoDB, and Elastic.

---

## 🛠️ How to Run (News Pipeline)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ibrand.git
cd ibrand/news-pipeline
```

### 2. Create `.env` File (optional for secrets)

Create a `.env` file if needed to store credentials (e.g., Mongo URI).

### 3. Start the Full Pipeline

```bash
docker-compose up --build
```

This will:

* Start Zookeeper, Kafka, MongoDB, Elasticsearch
* Launch Spark Master and Workers
* Run the Kafka producer to send news
* Submit the Spark job to consume news and save it to MongoDB

### 4. Verify MongoDB Storage

You can connect to MongoDB Atlas or use `mongosh` locally to check the `news-articles` collection in your cluster.

---

## 📦 Requirements

* Docker & Docker Compose
* A MongoDB Atlas URI (or local Mongo if preferred)
* Python 3.11+ (for local development and testing)

---
## 🧹 Modules in Progress
### 🔵 `frontend/`
* Will display generated posts
* UI to select brand voice
* Scheduled post suggestions
### 🟢 `backend/
The backend folder includes the following files and directories:
**app/**: Contains the main backend application modules and logic.
**emoji_api.py**: A standalone FastAPI emoji API with an initial /generate endpoint.
**index.py**: The main backend entrypoint, which starts the FastAPI app.
**.dockerignore**: Specifies files and folders to exclude from the backend Docker build context.
The backend is currently evolving with APIs supporting content generation and other AI-powered features.
## 📌 Future Additions

* Sentiment analysis and tone adaptation
* Integration with X, Instagram, Facebook APIs
* Scheduler to auto-post at peak times
* Brand tone learning module (via style input or samples)

---

## 💡 Summary

**iBrand** enables brands to stay ahead of trends by transforming real-time news into branded, high-engagement social media content. It's built for modern marketers looking to automate relevance at scale.

---

## 📬 Contact

# iBrand

iBrand is a smart content generation platform that helps brands and social media marketers catch trends early and generate catchy, engaging posts in their own brand voice. It does this by scraping trending news, enriching the data, and streaming it through a big data pipeline where personalized social media content is generated using AI and NLP.

---

## 🚀 Project Structure

```
iBrand/
├── backend/
│   └── index.py
├── frontend/
│   └── index.js
├── news-pipeline/
│   ├── kafka_app/
│   ├── scrapers/
│   ├── seed/
│   ├── spark/
│   ├── .dockerignore
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
```

---

## 🧠 How It Works (Pipeline Overview)

The `news-pipeline/` ingests and processes real-time news using the following stack:

* **Scrapers**: Pull trending news articles from multiple sources.
* **Kafka Producer**: Publishes news to a Kafka topic (`news-articles`).
* **Apache Spark**: A Spark Structured Streaming job reads the Kafka topic, parses the data, and writes enriched results to MongoDB.
* **MongoDB Atlas**: Stores the cleaned and structured news data.
* **Docker Compose**: Manages all services including Kafka, Spark, MongoDB, and Elastic.

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

### 🔵 `frontend/` – Coming Soon

* Will display generated posts
* UI to select brand voice
* Scheduled post suggestions

### 🟢 `backend/` – Coming Soon

* REST API for managing brand tone
* GPT-powered social copy generation
* Analytics and engagement predictor

---

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

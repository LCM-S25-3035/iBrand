# failsafe_metrics.py
import os, time, numpy as np
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

load_dotenv()  # reads your .env

MONGO_URI  = os.getenv("MONGO_URI") or os.getenv("MONGODB_URI") or ""
DB_NAME    = os.getenv("MONGO_DB", "articles-db")
COLL_NAME  = os.getenv("MONGO_COLL", "articles")
SAMPLE_N   = int(os.getenv("SAMPLE_N", "150"))
MAX_TEXT   = int(os.getenv("MAX_TEXT", "512"))

DEFAULT_MODELS = Path(__file__).resolve().parents[1] / "models"
MODELS_DIR = Path(os.getenv("MODELS_DIR", str(DEFAULT_MODELS))).resolve()

DISTIL = MODELS_DIR / "distilbert-base-uncased"
MINILM = MODELS_DIR / "all-MiniLM-L6-v2"
BART   = MODELS_DIR / "facebook-bart-large-mnli"

def pct(vals, q): return float(np.percentile(vals, q)) if vals else 0.0
def row(name, avg, p95): return f"{name:<18} | {avg:>8.3f} s | {p95:>8.3f} s"

def maybe_load_sentiment():
    try:
        from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
        tok = AutoTokenizer.from_pretrained(DISTIL.as_posix(), local_files_only=True)
        mod = AutoModelForSequenceClassification.from_pretrained(DISTIL.as_posix(), local_files_only=True)
        return pipeline("sentiment-analysis", model=mod, tokenizer=tok)
    except Exception as e:
        print(f"[skip] Sentiment load failed: {e}")
        return None

def maybe_load_tagging():
    try:
        from keybert import KeyBERT
        return KeyBERT(model=MINILM.as_posix())
    except Exception as e:
        print(f"[skip] Tagging (KeyBERT) load failed: {e}")
        return None

def maybe_load_bias():
    try:
        from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
        tok = AutoTokenizer.from_pretrained(BART.as_posix(), local_files_only=True)
        mod = AutoModelForSequenceClassification.from_pretrained(BART.as_posix(), local_files_only=True)
        return pipeline("zero-shot-classification", model=mod, tokenizer=tok)
    except Exception as e:
        print(f"[skip] Bias (zero-shot) load failed: {e}")
        return None

def main():
    if not MONGO_URI:
        print("ERROR: Missing MONGO_URI/MONGODB_URI in .env")
        return
    if not MODELS_DIR.is_dir():
        print(f"ERROR: MODELS_DIR not found: {MODELS_DIR}")
        return

    sentiment = maybe_load_sentiment()
    tagging   = maybe_load_tagging()
    bias      = maybe_load_bias()

    client = MongoClient(MONGO_URI)
    col = client[DB_NAME][COLL_NAME]
    docs = list(col.find({"content": {"$exists": True, "$type": "string", "$ne": ""}}, {"content": 1}).limit(SAMPLE_N))
    if not docs:
        print("No articles with non-empty 'content' found.")
        return

    t_sent, t_tags, t_bias, t_total = [], [], [], []
    bias_labels = ["left-leaning", "right-leaning", "neutral", "sensational", "factual"]
    LABEL_MAP = {"LABEL_0": "NEGATIVE", "LABEL_1": "POSITIVE"}

    start_all = time.perf_counter()
    for d in docs:
        text = (d.get("content") or "")[:MAX_TEXT]
        t0 = time.perf_counter()

        if sentiment:
            s0 = time.perf_counter()
            s = sentiment(text)[0]
            _ = LABEL_MAP.get(s.get("label", ""), s.get("label", ""))
            t_sent.append(time.perf_counter() - s0)

        if tagging:
            k0 = time.perf_counter()
            _ = tagging.extract_keywords(text, keyphrase_ngram_range=(1,2), stop_words="english", top_n=5)
            t_tags.append(time.perf_counter() - k0)

        if bias:
            b0 = time.perf_counter()
            _ = bias(text, bias_labels)
            t_bias.append(time.perf_counter() - b0)

        t_total.append(time.perf_counter() - t0)
    end_all = time.perf_counter()

    n = len(docs)
    throughput = n / (end_all - start_all)

    print("\n=== Inference Time (per article) ===")
    print("Stage              |   Avg (s) |   p95 (s)")
    print("-"*44)
    total_avg = float(np.mean(t_total)) if t_total else 0.0
    total_p95 = pct(t_total, 95)
    if sentiment: print(row("Sentiment", float(np.mean(t_sent)), pct(t_sent, 95)))
    if tagging:   print(row("Tagging",   float(np.mean(t_tags)), pct(t_tags, 95)))
    if bias:      print(row("Bias",      float(np.mean(t_bias)), pct(t_bias, 95)))
    print(row("TOTAL", total_avg, total_p95))
    print(f"\nThroughput: {throughput:.2f} articles/sec  (n={n})")
    print(f"DB: {DB_NAME}.{COLL_NAME}   MODELS_DIR: {MODELS_DIR}")

if __name__ == "__main__":
    main()

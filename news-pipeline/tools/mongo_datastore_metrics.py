# tools/mongo_datastore_metrics.py
# pip install "pymongo[srv]" dnspython
import os, time, json, statistics
from pymongo import MongoClient, ASCENDING, DESCENDING, TEXT
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Variables from .env
URI = os.getenv("MONGODB_URI")
DB = os.getenv("MONGO_DB", "articles-db")
COLL = os.getenv("MONGO_COLL", "articles")
LABEL = os.getenv("DATA_STORE_NAME", "MongoDB/News (articles-db.articles)")

client = MongoClient(URI, serverSelectionTimeoutMS=8000)
db = client[DB]; coll = db[COLL]

# --- DB/collection stats ---
dbs  = db.command("dbstats")
cols = db.command("collstats", COLL)
disk_usage_pct = round(100.0 * dbs["dataSize"] / dbs["storageSize"], 2) if dbs.get("storageSize") else None

# Ensure helpful indexes (no-op if already exist)
try:
    coll.create_index([("published_date", DESCENDING)])
    coll.create_index([("source", ASCENDING), ("published_date", DESCENDING)])
    coll.create_index([("title", TEXT), ("content", TEXT)])
except Exception:
    pass

now = time.time()

# Each entry RETURNS A CURSOR (no list() here)
def q_latest():
    return coll.find({}, {"_id": 1}).sort("published_date", -1).limit(20)

def q_source_week():
    return coll.find({"source": "TechCrunch"}, {"_id": 1}).sort("published_date", -1).limit(50)

def q_text_ai():
    return coll.find({"$text": {"$search": "AI"}}, {"_id": 1}).limit(20)

def q_sent_pos():
    return coll.find({"sentiment_label": "POSITIVE"}, {"_id": 1}).limit(50)

def q_date_24h():
    return coll.find({"published_date": {"$gte": now - 86400}}, {"_id": 1}).sort("published_date", -1).limit(100)

def q_source_date_combo():
    return coll.find({"source": "BBC", "published_date": {"$gte": now - 30*86400}}, {"_id": 1}).sort("published_date", -1).limit(100)

def q_by_id_sample():
    doc = coll.find_one({}, {"_id": 1})
    # build a cursor so .explain() exists
    return coll.find({"_id": doc["_id"]}, {"_id": 1}) if doc else coll.find({"_id": None})

queries = [
    ("latest", q_latest),
    ("source_week", q_source_week),
    ("text_AI", q_text_ai),
    ("sent_positive", q_sent_pos),
    ("date_last_24h", q_date_24h),
    ("source_date_combo", q_source_date_combo),
    ("by_id_sample", q_by_id_sample),
]

used_idx = 0
latencies = []

for name, qfn in queries:
    # ---- explain on CURSOR (no list()!) ----
    cursor_for_explain = qfn()
    plan = cursor_for_explain.explain().get("queryPlanner", {}).get("winningPlan", {})
    plan_txt = json.dumps(plan).upper()
    if "IXSCAN" in plan_txt or "TEXT" in plan_txt:
        used_idx += 1

    # ---- measure latency on a fresh cursor ----
    samples = []
    for _ in range(5):
        c = qfn()              # fresh cursor each timing run
        t0 = time.perf_counter()
        _ = list(c)            # execute
        samples.append((time.perf_counter() - t0) * 1000.0)
    latencies.append(statistics.mean(samples))

index_usage_pct = round(100.0 * used_idx / len(queries), 2)
avg_query_latency_ms = round(statistics.mean(latencies), 2)

result = {
    "data_store_name": LABEL,
    "index_usage_pct": index_usage_pct,
    "disk_usage_pct": disk_usage_pct,              # dataSize / storageSize (can be >100% due to compression)
    "avg_cpu_pct": None,                           # Atlas M0 → N/A
    "avg_memory_pct": None,                        # Atlas M0 → N/A
    "peak_open_connections": None,                 # Atlas M0 → N/A
    "peak_memory_mb": None,                        # Atlas M0 → N/A
    "error_rate_pct": None,                        # fill from app logs if needed

    # extras you can cite in footnotes
    "db_dataSize_bytes": int(dbs["dataSize"]),
    "db_storageSize_bytes": int(dbs["storageSize"]),
    "collection_count": int(cols["count"]),
    "avg_document_size_bytes": cols.get("avgObjSize"),
    "query_avg_latency_ms": avg_query_latency_ms
}

print(json.dumps(result, indent=2))
print("\nMarkdown row for your table:")
print(f"| {LABEL} | {index_usage_pct} | {disk_usage_pct} | N/A (M0) | N/A (M0) | N/A (M0) | N/A (M0) | N/A |")

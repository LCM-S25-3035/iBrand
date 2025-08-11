# news-pipeline/tools/scraper_metrics.py
# pip install "pymongo[srv]" dnspython pandas python-dotenv

import os, json, glob, statistics, datetime
from collections import defaultdict
from dotenv import load_dotenv
from pymongo import MongoClient
import pandas as pd

# ---------- Config / .env ----------
load_dotenv()

URI  = os.getenv("MONGODB_URI")
DB   = os.getenv("MONGO_DB", "articles-db")
COLL = os.getenv("MONGO_COLL", "articles")
LOG_DIR = os.getenv("SCRAPE_LOG_DIR", "./scrape/logs")  # optional

MANDATORY_FIELDS = ["url", "title", "content"]

if not URI:
    raise SystemExit("Set MONGODB_URI in .env (and optionally MONGO_DB, MONGO_COLL, SCRAPE_LOG_DIR).")

client = MongoClient(URI)
coll = client[DB][COLL]

now_utc = datetime.datetime.utcnow()
t24 = now_utc - datetime.timedelta(days=1)
t7  = now_utc - datetime.timedelta(days=7)

def to_ts(v):
    """Coerce numeric/ISO/datetime to epoch seconds; return None on failure."""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, datetime.datetime):
        return v.timestamp()
    s = str(v)
    try:
        return datetime.datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()
    except Exception:
        return None

# ---------- 1) Metrics from MongoDB ----------
def mongo_metrics(window_start=None):
    match = {}
    if window_start:
        # match either numeric epoch or datetime types
        match = {
            "$or": [
                {"published_date": {"$gte": window_start}},
                {"published_date": {"$gte": window_start.timestamp()}}
            ]
        }

    pipeline = [
        {"$match": match or {}},
        {"$group": {
            "_id": "$source",
            "count": {"$sum": 1},
            "missing": {"$sum": {
                "$cond": [
                    {"$or": [
                        {"$eq": ["$url", None]},
                        {"$eq": ["$title", None]},
                        {"$eq": ["$content", None]},
                        {"$not": ["$url"]},
                        {"$not": ["$title"]},
                        {"$not": ["$content"]}
                    ]},
                    1, 0
                ]
            }},
            "first_ts": {"$min": "$published_date"},
            "last_ts":  {"$max": "$published_date"},
        }},
        {"$project": {
            "_id": 0,
            "source": {"$ifNull": ["$_id", "Unknown"]},
            "pages_ok": "$count",
            "data_loss_pct": {"$cond": [
                {"$gt": ["$count", 0]},
                {"$multiply": [100.0, {"$divide": ["$missing", "$count"]}]},
                0
            ]},
            "first_ts": 1, "last_ts": 1
        }}
    ]

    rows = list(coll.aggregate(pipeline))
    out = []
    for r in rows:
        f_ts, l_ts = to_ts(r.get("first_ts")), to_ts(r.get("last_ts"))
        span = (l_ts - f_ts) if (f_ts and l_ts and l_ts > f_ts) else None
        tph = round(3600.0 * r["pages_ok"] / span, 2) if span else None
        out.append({
            "source": r["source"] or "Unknown",
            "pages_ok": r["pages_ok"],
            "data_loss_pct": round(float(r["data_loss_pct"]), 2),
            "throughput_per_hour": tph
        })
    return out

mongo_all = mongo_metrics(None)
mongo_7d  = mongo_metrics(t7)
mongo_24h = mongo_metrics(t24)

# ---------- 2) Optional JSONL logs ----------
def logs_metrics(log_dir):
    if not os.path.isdir(log_dir):
        return pd.DataFrame(columns=[
            "source","success_pct","blocked_captcha_pct","error_404_pct",
            "timeout_pct","throughput_per_hour","data_loss_pct",
            "resp_time_ms","pages_ok","total","ip_blocks_per_24h"
        ])

    records = []
    for path in glob.glob(os.path.join(log_dir, "*.jsonl")):
        site = os.path.splitext(os.path.basename(path))[0]
        total = ok = blocked = e404 = timeout = missing = 0
        elapsed = []
        scraped_ts = []
        ip_blocks = 0

        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                total += 1
                status = rec.get("status")
                tags = rec.get("tags") or {}
                if status == 200 and (all(tags.values()) if tags else True):
                    ok += 1
                if rec.get("blocked") or rec.get("captcha"):
                    blocked += 1
                if status == 404:
                    e404 += 1
                if rec.get("timeout"):
                    timeout += 1
                if not all(rec.get(k) for k in MANDATORY_FIELDS):
                    missing += 1
                if rec.get("elapsed_ms") is not None:
                    try:
                        elapsed.append(float(rec["elapsed_ms"]))
                    except Exception:
                        pass
                ts = rec.get("scraped_at")
                tsv = to_ts(ts)
                if tsv:
                    scraped_ts.append(tsv)
                if str(rec.get("error","")).lower().find("ip block") >= 0:
                    ip_blocks += 1

        if scraped_ts:
            scraped_ts.sort()
            span = max(1.0, scraped_ts[-1] - scraped_ts[0])
            tph = round(3600.0 * len(scraped_ts) / span, 2)
        else:
            tph = None

        records.append({
            "source": site,
            "success_pct": round(100.0 * ok / max(1, total), 2),
            "blocked_captcha_pct": round(100.0 * blocked / max(1, total), 2),
            "error_404_pct": round(100.0 * e404 / max(1, total), 2),
            "timeout_pct": round(100.0 * timeout / max(1, total), 2),
            "throughput_per_hour": tph,
            "data_loss_pct": round(100.0 * missing / max(1, total), 2),
            "resp_time_ms": round(statistics.mean(elapsed), 2) if elapsed else None,
            "pages_ok": ok,
            "total": total,
            "ip_blocks_per_24h": ip_blocks
        })

    return pd.DataFrame(records)

logs_df = logs_metrics(LOG_DIR)

# ---------- 3) Merge & present ----------
def df_from(rows, win_label):
    df = pd.DataFrame(rows)
    # Ensure source exists even if df is empty
    if df.empty:
        df = pd.DataFrame({"source": []})
    if "source" not in df.columns:
        df["source"] = "Unknown"
    rename = {
        "pages_ok": f"# Pages OK ({win_label})",
        "data_loss_pct": f"Data Loss % ({win_label})",
        "throughput_per_hour": f"Throughput (pages/hr, {win_label})"
    }
    return df.rename(columns=rename)

df_all  = df_from(mongo_all, "all")

# Build a stable base of sources from Mongo (so merges always have a key)
all_sources = sorted([s for s in coll.distinct("source") if s]) or ["Unknown"]
base = pd.DataFrame({"source": all_sources})

# Merge safely (left joins from base so 'source' always exists)
df = base.merge(df_all, on="source", how="left")

# Merge logs if present
if not logs_df.empty:
    df = df.merge(logs_df, on="source", how="left", suffixes=("", " (log)"))

# Order columns nicely if present
cols_order = [
    "source",
    "# Pages OK (all)", "Throughput (pages/hr, all)", "Data Loss % (all)",
    "# Pages OK (7d)",  "Throughput (pages/hr, 7d)",  "Data Loss % (7d)",
    "# Pages OK (24h)", "Throughput (pages/hr, 24h)", "Data Loss % (24h)",
    "success_pct", "blocked_captcha_pct", "error_404_pct", "timeout_pct",
    "resp_time_ms", "ip_blocks_per_24h", "total"
]
df = df.reindex(columns=[c for c in cols_order if c in df.columns]).sort_values(by="source", kind="stable")

def to_md(df):
    if df.empty:
        return "*(No data)*"
    out = ["| " + " | ".join(df.columns) + " |",
           "|" + "|".join(["---"]*len(df.columns)) + "|"]
    for _, row in df.iterrows():
        vals = []
        for v in row.tolist():
            if pd.isna(v):
                vals.append("")
            elif isinstance(v, float):
                # keep integers without .00
                vals.append(f"{v:.2f}".rstrip('0').rstrip('.'))
            else:
                vals.append(str(v))
        out.append("| " + " | ".join(vals) + " |")
    return "\n".join(out)

print("\n=== Scraper Metrics per Source ===\n")
print(to_md(df))

# ---------- Save CSVs ----------
os.makedirs("./metrics_out", exist_ok=True)
df.to_csv("./metrics_out/scraper_metrics.csv", index=False)
print("\nSaved CSVs under ./metrics_out/")

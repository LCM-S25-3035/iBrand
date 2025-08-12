from huggingface_hub import snapshot_download

# Download DistilBERT for Sentiment
snapshot_download(
    repo_id="distilbert/distilbert-base-uncased",
    local_dir="models/distilbert-base-uncased",
    local_dir_use_symlinks=False
)

# Download SentenceTransformer for Tag Extraction
snapshot_download(
    repo_id="sentence-transformers/all-MiniLM-L6-v2",
    local_dir="models/all-MiniLM-L6-v2",
    local_dir_use_symlinks=False
)

# Download BART for Zero-Shot Bias Detection
snapshot_download(
    repo_id="facebook/bart-large-mnli",
    local_dir="models/facebook-bart-large-mnli",
    local_dir_use_symlinks=False
)

print("All models downloaded successfully into the 'models/' folder.")

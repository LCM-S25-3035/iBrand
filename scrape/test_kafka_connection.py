from kafka import KafkaProducer

try:
    p = KafkaProducer(bootstrap_servers="localhost:9092")
    print("✅ Connected to Kafka!")
except Exception as e:
    print("❌ Failed to connect:", e)

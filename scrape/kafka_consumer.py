from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'news_topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='news-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("📡 Listening to news stream...")
for message in consumer:
    article = message.value
    print(f"\n📰 {article['title']}\n📎 {article['url']}")

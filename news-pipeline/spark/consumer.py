from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, ArrayType
from pyspark.sql.functions import from_json, col

MONGO_URI = "mongodb+srv://ernestyawgaisie:ernestyawgaisie@cluster0.dvjsafm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

spark = SparkSession.builder \
    .appName("KafkaToMongo") \
    .config("spark.mongodb.write.connection.uri", MONGO_URI) \
    .config("spark.mongodb.write.database", "newsdb") \
    .config("spark.mongodb.write.collection", "articles") \
    .getOrCreate()

# Define Kafka stream
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "news-articles") \
    .option("startingOffsets", "latest") \
    .load()

# Cast Kafka value to string
raw_df = df.selectExpr("CAST(value AS STRING) as json")

# Define schema
schema = StructType() \
    .add("title", StringType()) \
    .add("author", StringType()) \
    .add("published_at", StringType()) \
    .add("content", StringType()) \
    .add("url", StringType()) \
    .add("source", StringType()) \

# Parse JSON
parsed_df = raw_df.select(from_json(col("json"), schema).alias("data")).select("data.*")

# Write parsed data to console
# query = parsed_df.writeStream \
#     .outputMode("append") \
#     .format("console") \
#     .option("truncate", False) \
#     .start()


# Write stream to MongoDB
query = parsed_df.writeStream \
    .format("mongodb") \
    .option("checkpointLocation", "/tmp/spark-checkpoints/news") \
    .outputMode("append") \
    .start()

query.awaitTermination()

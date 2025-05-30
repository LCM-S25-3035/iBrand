from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, ArrayType
from pyspark.sql.functions import from_json, col

spark = SparkSession.builder \
    .appName("KafkaRawReader") \
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
    .add("id", StringType()) \
    .add("title", StringType()) \
    .add("author", StringType()) \
    .add("published_at", StringType()) \
    .add("content", StringType()) \
    .add("tags", ArrayType(StringType())) \
    .add("image_url", StringType()) \
    .add("url", StringType()) \
    .add("source", StringType()) \
    .add("scraped_at", StringType())

# Parse JSON
parsed_df = raw_df.select(from_json(col("json"), schema).alias("data")).select("data.*")

# Write parsed data to console
query = parsed_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", False) \
    .start()

query.awaitTermination()

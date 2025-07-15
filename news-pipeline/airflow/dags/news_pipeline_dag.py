from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
import sys
import os

# Add the root path if needed
sys.path.append('/opt/airflow')

default_args = {
    "owner": "airflow",
    "retries": 1,
}

with DAG(
    dag_id="news_pipeline_dag",
    default_args=default_args,
    start_date=datetime(2025, 6, 1),
    schedule_interval="@daily", 
    catchup=False,
    description="Scrape trending news, enrich data, and store in MongoDB via Spark",
) as dag:

    install_kafka = BashOperator(
        task_id="install_kafka_python",
        bash_command="pip install kafka-python"
    )

    start_producer = BashOperator(
        task_id="scrape_news_with_producer",
        bash_command="python /opt/airflow/kafka_app/producer_service.py"
    )

    run_enrichment = BashOperator(
        task_id="run_enrichment_script",
        bash_command="python /opt/airflow/enrichment/enrich_articles.py"
    )

    start_spark_consumer = BashOperator(
        task_id="run_spark_consumer",
        bash_command="spark-submit /opt/airflow/spark/spark_stream_consumer.py"
    )

    # Task sequence: install > scrape > enrich > store
    install_kafka >> start_producer >> run_enrichment >> start_spark_consumer

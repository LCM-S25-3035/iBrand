from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
import sys
import os

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
    description="Scrape trending news and send to Kafka",
) as dag:
    
    install_kafka = BashOperator(
        task_id="install_kafka_python",
        bash_command="pip install kafka-python"
    )


    start_producer = BashOperator(
        task_id="scrape_news_with_producer",
        bash_command="python /opt/airflow/kafka_app/producer_service.py"
    )

    install_kafka >> start_producer


@echo off
cd "C:\Kafka-docker"

REM Start Kafka (only if not already running)
docker-compose up -d

REM Run the data collection script
"C:\Users\c0937432\AppData\Local\Microsoft\WindowsApps\python.exe" newsapi_gnews_producer.py

pause

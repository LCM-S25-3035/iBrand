# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose the port your app runs on
EXPOSE 8000

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "emoji_api:app", "--host", "0.0.0.0", "--port", "8000"]

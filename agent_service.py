# -*- coding: utf-8 -*-
"""
main.py

This module implements a FastAPI service for generating engaging social media posts
from enriched news articles. It integrates with MongoDB to fetch article data
and uses Google Gemini (LLM) to create posts based on dynamic prompts,
inferred tone, and emoji preferences.

This version uses FastAPI's recommended 'lifespan' event handlers for managing
application startup and shutdown, resolving DeprecationWarnings.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import os
import requests
from pymongo import MongoClient
from bson.objectid import ObjectId # Required if _id is ObjectId type
from dotenv import load_dotenv # Used to load environment variables from .env file
import contextlib # Import for asynccontextmanager

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
# Fetch credentials from environment variables for security.
# Ensure these are set in your .env file or your deployment environment.
MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "articles-db") # Default if not set in .env
MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME", "articles") # Default if not set in .env

GOOGLE_GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GOOGLE_GEMINI_API_KEY}"

# --- MongoDB Setup (Global variables for collection and client) ---
articles_collection = None
mongo_client = None

# --- Lifespan Event Handler ---
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages the lifespan of the FastAPI application, handling database connection
    during startup and graceful disconnection during shutdown.
    """
    global articles_collection, mongo_client
    try:
        # --- Startup Logic ---
        if not MONGO_CONNECTION_STRING:
            raise ValueError("MONGO_CONNECTION_STRING environment variable is not set. Please check your .env file.")
        if not GOOGLE_GEMINI_API_KEY:
            raise ValueError("GOOGLE_GEMINI_API_KEY environment variable is not set. Please check your .env file.")

        mongo_client = MongoClient(MONGO_CONNECTION_STRING)
        # Ping the MongoDB server to confirm a successful connection and authentication
        mongo_client.admin.command('ping')
        db = mongo_client[MONGO_DB_NAME]
        articles_collection = db[MONGO_COLLECTION_NAME]
        print("Successfully connected to MongoDB and retrieved articles collection during startup.")
        
        # Yield control to the application, allowing it to start processing requests
        yield
        
    except Exception as e:
        print(f"FATAL ERROR: Failed to connect to MongoDB or load credentials during startup: {e}")
        # Re-raise the exception to prevent the application from starting if critical resources fail
        raise
    finally:
        # --- Shutdown Logic (executed when the application stops) ---
        if mongo_client:
            mongo_client.close()
            print("MongoDB connection closed during shutdown.")

# --- FastAPI App Initialization ---
# The lifespan argument registers the async context manager for application lifecycle events.
app = FastAPI(
    title="Agentic Social Media Post Generator",
    description="Service to generate engaging social media posts from news articles using LLMs.",
    version="1.0.0",
    lifespan=lifespan # Assign the lifespan manager to the app
)

# --- Pydantic Models for Request Body Validation ---
class PostGenerationRequest(BaseModel):
    """
    Request model for generating a social media post.
    """
    article_id: str = Field(..., description="The MongoDB ObjectId string of the news article.")
    override_tone: Optional[str] = Field(None, description="Optional: Force a specific tone (e.g., 'humorous', 'professional'). Overrides inferred tone.")
    include_emojis: bool = Field(False, description="If true, include relevant emojis in the generated post.")

# --- Core LLM Helper Functions ---

def infer_tone_from_sentiment(sentiment_label: str, bias_label: str = None) -> str:
    """
    Infers a suitable social media post tone based on the article's sentiment label
    and optionally its bias label. This tone guides the LLM in generation.
    """
    sentiment_label = sentiment_label.upper()

    if sentiment_label == "POSITIVE":
        return "enthusiastic and promotional"
    elif sentiment_label == "NEGATIVE":
        if bias_label and bias_label.lower() == "sensational":
            return "alarming and cautionary"
        return "critical and concerned"
    elif sentiment_label == "NEUTRAL":
        return "informative and objective"
    else:
        return "informative"

def build_prompt(article_data: dict, tone: str, include_emojis: bool = False) -> str:
    """
    Constructs a dynamic prompt for the LLM, emphasizing the creation of highly engaging,
    human-like social media posts with attention-grabbing elements and calls to action.
    """
    title = article_data.get('title', 'A recent news event')
    summary = article_data.get('summary', 'No summary available.')
    tags = ", ".join(article_data.get('tags', []))
    sentiment_label = article_data.get('sentiment', {}).get('label', 'N/A')
    bias_label = article_data.get('bias', {}).get('label', 'N/A')
    source = article_data.get('source', 'an unknown source')

    prompt_parts = [
        f"Your task is to craft a **highly engaging, concise, and human-like social media post** based on the following news article.",
        f"The post should prominently feature a **{tone}** tone and be designed to grab immediate attention."
    ]

    prompt_parts.append(f"\n**Article Details:**")
    prompt_parts.append(f"**Title:** {title}")
    prompt_parts.append(f"**Summary:** {summary}")

    if tags:
        prompt_parts.append(f"**Keywords/Topics:** {tags}")
    if sentiment_label != 'N/A':
        prompt_parts.append(f"**Detected Sentiment:** {sentiment_label}")
    if bias_label != 'N/A':
        prompt_parts.append(f"**Detected Bias:** {bias_label}")
    if source:
        prompt_parts.append(f"**Source:** {source}")

    prompt_parts.append("\n**Instructions for the Post:**")
    prompt_parts.append("- **Length:** Keep it very concise (1-3 impactful sentences, suitable for a tweet or short status update).")
    prompt_parts.append("- **Hook:** Start with a strong, attention-grabbing hook, question, or surprising statement.")
    prompt_parts.append("- **Language:** Use clear, conversational, and human-like language that resonates with a general audience.")
    prompt_parts.append("- **Focus:** Highlight the most important takeaway or intriguing aspect of the article.")
    prompt_parts.append("- **No External Links:** Do NOT include any external links, URLs, or hashtags in the post itself.")

    if "promotional" in tone.lower() or "informative" in tone.lower() or "objective" in tone.lower():
        prompt_parts.append("- **Call to Action (Optional):** If appropriate for the tone, end with a subtle, general call to action (e.g., 'Share your thoughts!', 'Stay informed!', 'What do you think?').")
    elif "critical" in tone.lower() or "alarming" in tone.lower() or "concerned" in tone.lower():
        prompt_parts.append("- **Call to Action (Optional):** If appropriate for the tone, encourage awareness, discussion, or vigilance (e.g., 'Stay vigilant!', 'Your thoughts?', 'Don't miss this!').")

    if include_emojis:
        prompt_parts.append("- **Emojis:** Include 1-3 highly relevant and appropriate emojis to enhance visual appeal and engagement.")
    else:
        prompt_parts.append("- **No Emojis:** Do NOT include any emojis.")

    prompt_parts.append("\nGenerate **only** the social media post text. Do not add any introductory phrases (e.g., 'Here's your post:') or concluding remarks.")

    final_prompt = "\n".join(prompt_parts)
    return final_prompt

# --- FastAPI Endpoints ---

@app.post("/generate_social_media_post/")
async def generate_social_media_post_endpoint(request_data: PostGenerationRequest):
    """
    Generates an engaging social media post for a specified article ID.
    You can override the inferred tone and choose to include emojis.
    """
    # Ensure articles_collection is available after startup
    if articles_collection is None:
        raise HTTPException(status_code=500, detail="Database connection not established. Check server startup logs.")
    if not GOOGLE_GEMINI_API_KEY:
         raise HTTPException(status_code=500, detail="Google Gemini API Key is not configured.")

    try:
        # Convert the article_id string from the request to a MongoDB ObjectId
        article_obj_id = ObjectId(request_data.article_id)
        article_data = articles_collection.find_one({"_id": article_obj_id})

        if not article_data:
            raise HTTPException(status_code=404, detail=f"Article with ID '{request_data.article_id}' not found.")

        # Determine the final tone to use
        if request_data.override_tone:
            final_tone = request_data.override_tone
        else:
            sentiment_label = article_data.get('sentiment', {}).get('label', 'NEUTRAL')
            bias_label = article_data.get('bias', {}).get('label')
            final_tone = infer_tone_from_sentiment(sentiment_label, bias_label)

        print(f"--- Generating post for article ID: {request_data.article_id} with tone: {final_tone} and emojis: {request_data.include_emojis} ---")

        # Build the prompt for the LLM
        llm_prompt = build_prompt(article_data, final_tone, request_data.include_emojis)

        # Prepare payload for Gemini API
        payload = {
            "contents": [
                {"role": "user", "parts": [{"text": llm_prompt}]}
            ],
            "generationConfig": {
                "temperature": 0.9,
                "maxOutputTokens": 100
            }
        }

        # Make the API call to Gemini
        response = requests.post(GEMINI_API_URL, headers={'Content-Type': 'application/json'}, json=payload)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

        result = response.json()

        if result.get('candidates') and result['candidates'][0].get('content') and result['candidates'][0]['content'].get('parts'):
            generated_text = result['candidates'][0]['content']['parts'][0]['text']
            return {"post": generated_text}
        else:
            print(f"LLM response structure unexpected: {result}")
            raise HTTPException(status_code=500, detail="Failed to generate post: Unexpected LLM response structure.")

    except HTTPException as he:
        # Re-raise FastAPI's HTTPExceptions directly
        raise he
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Invalid article ID format: {ve}")
    except requests.exceptions.RequestException as re:
        raise HTTPException(status_code=502, detail=f"Failed to connect to LLM API: {re}. Check API key and network.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {e}")


# --- Health Check Endpoint (Optional but Recommended) ---
@app.get("/health/")
async def health_check():
    """
    Health check endpoint to verify service status and database connectivity.
    """
    try:
        # Ensure articles_collection is available before attempting DB operation
        if articles_collection:
            # Attempt a simple database operation (e.g., count documents) to check connectivity
            articles_collection.count_documents({})
            db_status = "Connected"
        else:
            db_status = "Disconnected (not initialized or failed during startup)"
        
        # Check if API key is loaded
        api_key_status = "Loaded" if GOOGLE_GEMINI_API_KEY else "Missing"

        return {"status": "ok", "database_connection": db_status, "gemini_api_key_status": api_key_status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {e}")


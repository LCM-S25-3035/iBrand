import httpx
from typing import Optional

class EmojiGenClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key  # if your API needs auth

    async def enrich(self, text: str, mood: Optional[str] = None) -> dict:
        payload = {"text": text}
        if mood:
            payload["mood"] = mood

        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/generate", json=payload, headers=headers)
            response.raise_for_status()
            return response.json()

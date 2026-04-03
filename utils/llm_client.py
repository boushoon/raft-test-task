import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

# Конфигурация
API_KEY = os.getenv("API_KEY")
FOLDER_ID = os.getenv("FOLDER_ID")
MODEL = os.getenv("MODEL")


def call_llm(prompt: str, system_prompt: str) -> str:
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

    headers = {
        "Authorization": f"Api-Key {API_KEY}",
        "Content-Type": "application/json"
    }

    messages = [
        {"role": "system", "text": system_prompt},
        {"role": "user", "text": prompt}
    ]

    body = {
        "modelUri": f"gpt://{FOLDER_ID}/{MODEL}/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.0
        },
        "messages": messages
    }

    response = requests.post(url, headers=headers, json=body)
    result = response.json()

    # Достаём текст
    text = result["result"]["alternatives"][0]["message"]["text"].strip("`").strip()

    return json.loads(text)

import requests
import json
from dotenv import dotenv_values

from config import SYSTEM_PROMPT_FOR_TAG_LLM


API_KEY = dotenv_values('.env')['OPEN_ROUTER_API_KEY']

def sort_tags(title: str, tags: list):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "deepseek/deepseek-r1-0528:free",
            "messages": [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT_FOR_TAG_LLM
                },
                {
                    "role": "user",
                    "content": f"Title of the article: {title}\nList of Tags: {' | '.join(tags)}"
                }
            ],

        })
    )
    print(response.json()["choices"][0]["message"]["content"])
    input("Press Enter to continue...")

sort_tags("US Federal Reserve Holds Interest Rates Steady Amid Economic Uncertainty", ["USA", "Economy", "Finance", "Politics", "Banking"])
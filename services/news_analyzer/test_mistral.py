import requests
import json
from dotenv import dotenv_values


API_KEY = dotenv_values('.env')['OPEN_ROUTER_API_KEY']

def deepseek():
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
                    "role": "user",
                    "content": f"Can you say what in this link ? What theme the video about ?"
                }
            ],

        })
    )
    print(response.json()["choices"][0]["message"]["content"])
    input("Press Enter to continue...")

deepseek()
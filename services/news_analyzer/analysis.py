import requests
import json
import re
from pathlib import Path
from io import BytesIO
from dotenv import dotenv_values
from models import RawArticle

import config

dotenv = dotenv_values('.env')
API_KEY = dotenv['OPEN_ROUTER_API_KEY']
WEBUI_API = dotenv['WEBUI_API']
WEBUI_API_TAGS =dotenv['WEBUI_API_TAGS']

BASE_DIR = Path(__file__).resolve().parents[2]
TOKEN_DOTENV_PATH = BASE_DIR / ".env"
TOKEN = dotenv_values(TOKEN_DOTENV_PATH)["neural_network_user_token"]

def slugify(s):
  s = s.lower().strip()
  s = re.sub(r'[^\w\s-]', '', s)
  s = re.sub(r'[\s_-]+', '-', s)
  s = re.sub(r'^-+|-+$', '', s)
  return s

def send_to_webui(analyzed_article):
    print("[WEBUI SENDER] Start process new article ...")
    match = re.search(r"src=['\"](.*?)['\"]", analyzed_article["title_image"])
    if match:
        img_url = match.group(1)
        response = requests.get(img_url)
        if response.status_code == 200:
            headers = {"Authorization": f"Token {TOKEN}"}

            image_bytes = BytesIO(response.content)
            image_bytes.name = "title_image.webp"

            tags = []
            for tag in analyzed_article["tags"]:
                slug = slugify(tag)
                response = requests.get(WEBUI_API_TAGS + slug, headers=headers)
                if response.status_code == 200:
                    tags.append(response.json()["id"])
                else:
                    response = requests.post(WEBUI_API_TAGS, json={
                        "name": tag,
                        "slug": slug,
                    }, headers=headers)
                    if response.status_code == 201:
                        tags.append(response.json()["id"])
                    else:
                        print(response.content)
                        print("[WEBUI SENDER] [ERROR] Failed to create tag for article")

            files = {
                "image": image_bytes
            }
            data = {
                "title": analyzed_article["title"],
                "slug": analyzed_article["slug"],
                "summary": analyzed_article["summary"],
                "content": analyzed_article["html"],
                "category": config.CATEGORIES[analyzed_article["category"]],
                "tags": tags
            }
            print("[WEBUI SENDER] Sending to web_ui ...")
            res = requests.post(WEBUI_API, data=data, files=files, headers=headers)
            if res.status_code == 201:
                print("[WEBUI SENDER] Article sent -", res)
            else:
                print("[WEBUI SENDER] Article sending failed -", res, res.content)
    else:
        print("[WEBUI SENDER][ERROR] Match is null")

def llm_analyze_article(raw_article: RawArticle):
    print("[ANALYZER] Process article...")
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
                    "content": config.SYSTEM_PROMPT_FOR_LLM_2
                },
                {
                    "role": "user",
                    "content": f"html: {raw_article.html}, category: {raw_article.category}"
                }
            ],
        })
    )
    print("[ANALYZER] Response content -", response.content)
    raw = response.json()["choices"][0]["message"]["content"]
    print("[ANALYZER] Done")
    print("[ANALYZER] Raw\n", raw)
    print("[ANALYZER] Raw type:", type(raw))
    raw_dict = json.loads(raw)
    raw_dict["html"] = raw_dict["html"].replace("\n", "")

    print("[ANALYZER] Returned")
    return raw_dict

def process_article(raw_article: RawArticle):
    analyzed_article = llm_analyze_article(raw_article)
    send_to_webui(analyzed_article)


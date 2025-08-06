from pathlib import Path
from types import NoneType
from io import BytesIO
import requests
import json
import re
import os
from dotenv import load_dotenv

from models import RawArticle
import config
from logger import get_logger

logger = get_logger()

root = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=root / ".env")
if os.getenv("DOCKER") == "false":
    load_dotenv(dotenv_path=root / ".env.local", override=True)

API_KEY = os.environ['OPEN_ROUTER_API_KEY_1']
WEBUI_API = os.environ['WEBUI_API']
WEBUI_API_TAGS = os.environ['WEBUI_API_TAGS']
TOKEN = os.environ["neural_network_user_token"]
WEBUI_API_REGION = os.environ['WEBUI_API_REGION']


def slugify(s):
    s = s.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_-]+', '-', s)
    s = re.sub(r'^-+|-+$', '', s)
    return s


def send_message_to_llm(system_prompt, content):
    logger.info("[ANALYZER] Sending article to llm")
    return requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "deepseek/deepseek-r1-0528:free", # deepseek/deepseek-r1-0528:free | deepseek/deepseek-chat-v3-0324:free
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": content
                }
            ],
        })
    )


def send_to_webui(analyzed_article):
    logger.info("[WEBUI SENDER] Start process new article")
    if analyzed_article in [NoneType, None]:
        logger.error("[WEBUI SENDER][ERROR] title_image is null")
        return None
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
                        logger.info(response.content)
                        logger.error("[WEBUI SENDER] [ERROR] Failed to create tag for article")

            region = requests.get(f'{WEBUI_API_REGION}{analyzed_article["region"]}')
            files = {
                "image": image_bytes
            }
            data = {
                "title": analyzed_article["title"],
                "slug": analyzed_article["slug"],
                "summary": analyzed_article["summary"],
                "content": analyzed_article["html"],
                "category": config.CATEGORIES[analyzed_article["category"]],
                "tags": tags,
                "region": region.json()["id"],
            }
            logger.info("[WEBUI SENDER] Sending to web_ui")
            res = requests.post(WEBUI_API, data=data, files=files, headers=headers)
            if res.status_code == 201:
                logger.info(f"[WEBUI SENDER] Article sent - {res}")
                return res
            else:
                logger.error(f"[WEBUI SENDER] Article sending failed - {res} {res.content}")
                return res
    else:
        logger.error("[WEBUI SENDER][ERROR] Match is null")


def llm_analyze_article(raw_article: RawArticle):
    logger.info("[ANALYZER] Processing article")
    response = send_message_to_llm(config.SYSTEM_PROMPT_FOR_LLM, f"html: {raw_article.html}, category: {raw_article.category}")
    try:
        raw = response.json()["choices"][0]["message"]["content"]
        # logger.info("[ANALYZER] Done")
        # logger.info("[ANALYZER] Raw\n", raw)
        # logger.info("[ANALYZER] Raw type:", type(raw))
        raw_dict = json.loads(raw)
        raw_dict["html"] += f"<p>Source: <a href=\"{raw_article.guid}\">Original Article</a></p>"
        raw_dict["html"] = raw_dict["html"].replace("\n", "")
        logger.info("[ANALYZER] Returned")
        return raw_dict
    except Exception as e:
        logger.error(f"[ANALYZER][ERROR] {e}")
        logger.info(response.json())


def process_article(raw_article: RawArticle):
    try:
        analyzed_article = llm_analyze_article(raw_article)
    except json.decoder.JSONDecodeError:
        analyzed_article = llm_analyze_article(raw_article)

    send_to_webui(analyzed_article)


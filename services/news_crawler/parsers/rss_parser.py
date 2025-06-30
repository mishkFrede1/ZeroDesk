from datetime import datetime
from random import randint
from types import NoneType
import feedparser
import requests
from bs4 import BeautifulSoup

from logger import get_logger
from config import HEADERS
from database import is_article_exists, save_article

logger = get_logger()

class RSSParser:
    article_main_object_find_type = None
    article_main_object = None
    title_image_separated = False
    title_image_object_class = None

    def __init__(self, sys_name: str, categories: dict, guid: bool):
        self.sys_name = sys_name
        self.name = sys_name.lower()
        self.categories = categories
        self.guid = guid

    def parse_all(self, articles_count: int):
        logger.info(f"[{self.sys_name} PARSER] Started parsing {self.name}...")
        articles = []
        for category in self.categories:
            articles += self._parse_category(category["url"], category["category"], articles_count, self.guid)
        return articles

    def _parse_category(self, url: str, category: str, articles_count: int, guid: bool):
        feed = feedparser.parse(url)
        logger.info(f"[{self.sys_name} PARSER] Start parsing {category}")


        articles = []
        index = 0
        if guid:
            for entry in feed.entries:
                # print(f"[{self.sys_name} PARSER]", entry.guid, is_article_exists(entry.guid))
                if "live-news" in entry.guid or "videos" in entry.guid or "sounds" in entry.guid or "iplayer" in entry.guid or is_article_exists(entry.guid):
                    continue
                parsed_article = self._parse_article(entry.guid, category)
                if parsed_article is not None: articles.append(parsed_article)
                if index >= articles_count: break
                index += 1
        else:
            for entry in feed.entries:
                if "live-news" in entry.link or "videos" in entry.link or "sounds" or "iplayer" in entry.link in entry.link or is_article_exists(entry.link):
                    continue
                parsed_article = self._parse_article(entry.link, category)
                if parsed_article is not None: articles.append(parsed_article)
                if index >= articles_count: break
                index += 1
        return articles

    def _parse_article(self, guid: str, category: str):
        response = requests.get(guid, headers=HEADERS)
        soup = BeautifulSoup(response.content, "html.parser")

        article_html = ""
        title_tag = soup.find("h1")
        if title_tag:
            title = f"<h1>{title_tag.get_text(strip=True)}</h1>\n"
            article_html += title + "\n"
        else:
            logger.error(f"[{self.sys_name} PARSER] title_tag not found.")
            return None

        if self.article_main_object_find_type.lower() == "class":
            article = soup.find(attrs={"class": self.article_main_object})
        else:
            article = soup.find(self.article_main_object)

        if not article:
            logger.error(f"[{self.sys_name} PARSER] Не удалось найти article - {guid}")
            return None

        if self.title_image_separated:
            title_image_block = soup.find(attrs={"class": self.title_image_object_class})
            if title_image_block:
                for element in article.descendants:
                    if element.name == 'img':
                        high_quality_src = self._get_max_quality_srcset(element)
                        alt = element.get("alt", "")
                        if high_quality_src:
                            img_tag = f'<img src="{high_quality_src}" alt="{alt}">\n'
                            article_html += img_tag


        article_html += self.parse_article_html(article, guid)

        if article_html is None:
            return None

        save_article(guid, title, datetime.now())
        html = article_html.strip()
        return {
            "guid": guid,
            "html": html,
            "category": category,
            "source": self.name
        }

    def parse_article_html(self, article, guid: str):
        """
        You have to write YOUR html page parser in this function
        :param guid: Article's guid or link.
        :return article_html: html string with tags: <h2>, <p>, <img>.
        """
        article_html = ""
        return article_html

    def parse_article_and_get_debug(self, guid: str, category: str):
        parsed_article = self._parse_article(guid, category)
        if parsed_article:
            formatted = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            with open(f"parsers/debug_html/{self.sys_name}_{category}_{formatted}.html", "w", encoding="utf-8") as f:
                f.write(parsed_article["html"])

            return parsed_article
        else:
            logger.error(f"[{self.sys_name} PARSER] Error during the parsing.")
            return None

    @staticmethod
    def check_class(class_: list, bad_classes):
        if type(class_) is not NoneType:
            for c in class_:
                if c in bad_classes:
                    return True
        return False

    @staticmethod
    def delete_block_by_class(article, classes: str):
        for block in article.select(classes):
            block.decompose()
        return article

    @staticmethod
    def _get_max_quality_srcset(img_tag, extra_split=False):
        # 1. Получаем srcset
        srcset = img_tag.get("srcset")
        if not srcset:
            return img_tag.get("src")  # fallback

        # 2. Парсим все варианты
        candidates = []
        if extra_split:
            items = []
            set_ = srcset.split(",")
            for i in range(0, len(set_) - 1, 2):
                items.append(set_[i] + "," + set_[i + 1])
        else:
            items = srcset.split(",")

        for item in items:
            parts = item.strip().split(" ")
            if len(parts) == 2:
                url, width = parts
                try:
                    width = int(width.rstrip("w"))
                    candidates.append((width, url))
                except ValueError:
                    continue

        # 3. Берем URL с максимальной шириной
        if candidates:
            candidates.sort(reverse=True)  # по ширине
            return candidates[0][1]
        return img_tag.get("src")
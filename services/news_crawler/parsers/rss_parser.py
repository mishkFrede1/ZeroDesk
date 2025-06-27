from datetime import datetime
from random import randint
import feedparser
import requests
from bs4 import BeautifulSoup

from config import HEADERS
from database import is_article_exists, save_article

class RSSParser:
    def __init__(self, sys_name: str, categories: dict, guid: bool):
        self.sys_name = sys_name
        self.name = sys_name.lower()
        self.categories = categories
        self.guid = guid

    def parse_all(self, articles_count: int):
        print(f"[{self.sys_name} PARSER]: Started parsing {self.name}...")
        articles = []
        for category in self.categories:
            articles += self._parse_category(category["url"], category["category"], articles_count, self.guid)
        return articles

    def _parse_category(self, url: str, category: str, articles_count: int, guid: bool):
        feed = feedparser.parse(url)
        print(f"[{self.sys_name} PARSER]: Start parsing", category)


        articles = []
        index = 0
        if guid:
            for entry in feed.entries:
                print(f"[{self.sys_name} PARSER]", entry.guid, is_article_exists(entry.guid))
                if "live-news" in entry.guid or "videos" in entry.guid or is_article_exists(entry.guid):
                    continue
                parsed_article = self._parse_article(entry.guid, category)
                if parsed_article is not None: articles.append(parsed_article)
                if index >= articles_count: break
                index += 1
        else:
            for entry in feed.entries:
                print(f"[{self.sys_name} PARSER]", entry.link, is_article_exists(entry.link))
                if "live-news" in entry.link or "videos" in entry.link or is_article_exists(entry.link):
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
            print(f"[{self.sys_name} PARSER][ERROR] title_tag not found.", )
            return None

        article_html += self.parse_article_html(soup, guid)

        save_article(guid, title, datetime.now())
        html = article_html.strip()
        return {
            "guid": guid,
            "html": html,
            "category": category,
            "source": self.name
        }

    def parse_article_html(self, soup: BeautifulSoup, guid: str):
        """
        You have to write YOUR html page parser in this function
        :param soup: BeautifulSoup() class object.
        :param guid: Article's guid or link.
        :return article_html: html string with tags: <h2>, <p>, <img>.
        """
        article_html = ""
        return article_html

    @staticmethod
    def _get_max_quality_srcset(img_tag):
        # 1. Получаем srcset
        srcset = img_tag.get("srcset")
        if not srcset:
            return img_tag.get("src")  # fallback

        # 2. Парсим все варианты
        candidates = []
        for item in srcset.split(","):
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

    def parse_article_and_get_debug(self, guid: str, category: str):
        parsed_article = self._parse_article(guid, category)

        formatted = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        source = self.sys_name.replace(' ', '_')
        with open(f"parsers/debug_html/{source}_{category}_{formatted}.html", "w", encoding="utf-8") as f:
            f.write(parsed_article["html"])

        return parsed_article
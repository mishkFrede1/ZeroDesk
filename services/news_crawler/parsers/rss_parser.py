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
    sys_name = "RSSParserDefaultName"
    categories = None
    guid = True

    article_main_object_find_type = ""
    article_main_object = None

    title_image_separated = False
    title_image_object_class = None
    img_extra_split = False

    bad_blocks = None
    bad_url_patterns = []

    # GENERAL PARSING
    def parse_all(self, articles_count: int):
        logger.info(f"[{self.sys_name} PARSER] Started parsing {self.sys_name.lower()}...")
        articles = []
        for category in self.categories:
            articles += self._parse_category(category["url"], category["category"], articles_count, self.guid)
        return articles

    def _parse_category(self, url: str, category: str, articles_count: int, guid: bool):
        feed = feedparser.parse(url)
        logger.info(f"[{self.sys_name} PARSER] Start parsing {category}")


        articles = []
        index = 0
        if self.guid:
            for entry in feed.entries:
                # "live-news" in entry.guid or "videos" in entry.guid or "sounds" in entry.guid or "iplayer" in entry.guid
                if is_article_exists(entry.guid) or self._article_validation_url(entry.guid):
                    continue
                parsed_article = self.parse_article_and_get_debug(entry.guid, category)
                if parsed_article is not None: articles.append(parsed_article)
                if index >= articles_count: break
                index += 1
        else:
            for entry in feed.entries:
                if is_article_exists(entry.link) or self._article_validation_url(entry.link):
                    continue
                parsed_article = self.parse_article_and_get_debug(entry.link, category)
                if parsed_article is not None: articles.append(parsed_article)
                if index >= articles_count: break
                index += 1
        return articles

    # ARTICLE'S HTML PARSING METHODS
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
                        article_html = self.img_high_quality_parsing(article_html, element)

        if self.bad_blocks and type(self.bad_blocks) == list:
            for bad_element in self.bad_blocks:
                article = self.delete_block_by_class(article, bad_element)

        article_html += self.parse_article_html(article)

        if article_html is None:
            return None

        save_article(guid, title, datetime.now())
        html = article_html.strip()
        return {
            "guid": guid,
            "html": html,
            "category": category,
            "source": self.sys_name.lower()
        }

    def parse_article_html(self, article):
        article_html = ""

        for element in article.descendants:
            if element.name == 'p' and self.extra_validation_p(element):
                article_html += f"<p>{element.get_text(strip=True)}</p>\n"

            elif element.name == 'h2' and self.extra_validation_h2(element):
                article_html += f"<h2>{element.get_text(strip=True)}</h2>\n"

            elif element.name == 'img':
                article_html = self.img_high_quality_parsing(article_html, element)

            extra_validation = self.extra_validation_element(article_html, element)
            if extra_validation:
                article_html = extra_validation

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

    def img_high_quality_parsing(self, article_html, element):
        high_quality_src = self._get_max_quality_srcset(element)
        alt = element.get("alt", "")
        if high_quality_src and self.extra_validation_img(element, high_quality_src):
            img_tag = f'<img src="{high_quality_src}" alt="{alt}">\n'
            article_html += img_tag

        return article_html

    # VALIDATION METHODS
    def _article_validation_url(self, url: str):
        for bad in self.bad_url_patterns:
            if bad in url: return True
        return False

    # EXTRA VALIDATION METHODS
    @staticmethod
    def extra_validation_element(article_html, element):
        """
        Write here extra validation for other html elements
        :param article_html: main output html
        :param element: html element from loop
        :return article_html: return new article_html
        """
        return None

    @staticmethod
    def extra_validation_img(element, src):
        """
        Write here your extra <imh> tags validation.
        :param element: <img> tag element
        :param src: <img> tag src attribute
        :return: Boolean
        """
        return True

    @staticmethod
    def extra_validation_p(element):
        """
        Write here your extra <p> tags validation
        :param element: <p> tag element
        :return: Boolean
        """
        return True

    @staticmethod
    def extra_validation_h2(element):
        """
        Write here your extra <h2> tags validation
        :param element: <h2> tag element
        :return: Boolean
        """
        return True

    # EXTRA FUNCTIONAL
    @staticmethod
    def check_class(class_: list, bad_classes):
        if type(class_) is not NoneType:
            for c in class_:
                if c in bad_classes: return True
        return False

    @staticmethod
    def delete_block_by_class(article, classes: str):
        for block in article.select(classes):
            block.decompose()
        return article

    def _get_max_quality_srcset(self, img_tag):
        # 1. Получаем srcset
        srcset = img_tag.get("srcset")
        if not srcset:
            return img_tag.get("src")  # fallback

        # 2. Парсим все варианты
        candidates = []
        if self.img_extra_split:
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
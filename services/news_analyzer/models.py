from pydantic import BaseModel

class RawArticle(BaseModel):
    guid: str
    html: str
    category: str
    source: str

class ProcessedArticle(BaseModel):
    html_content: str
    category: str
    tags: list[str]

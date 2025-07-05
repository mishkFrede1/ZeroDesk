from fastapi import APIRouter

from logger import get_logger
from analysis import process_article
from models import RawArticle

logger = get_logger()

router = APIRouter()
@router.post("/analyze-article/")
def analyze_article(request: RawArticle):
    logger.info(f"[INFO] Article sent to analyzer: {request.guid}")
    return process_article(request)

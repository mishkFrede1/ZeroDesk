from http.client import HTTPResponse

from fastapi import APIRouter

from analysis import process_article
from models import RawArticle

router = APIRouter()
@router.post("/analyze-article/")
def analyze_article(request: RawArticle):
    print("[INFO] Article sent to analyzer:", request.guid)
    return process_article(request)

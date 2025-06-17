from fastapi import FastAPI
from api import router
app = FastAPI(title="News Analyzer API")
app.include_router(router)

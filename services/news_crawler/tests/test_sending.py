import requests_mock
from utils.sender import send_to_analyzer

article = {"guid":"123", "html": "<h2>Test Article</h2>", "category": "politics", "source": "news"}

def test_send_to_analyzer():
    with requests_mock.Mocker() as mock:
        mock.post("http://localhost:80/analyze-article/", json={"status": "ok"}, status_code=200)

        response = send_to_analyzer(article)
        assert response[1].ok
        assert response[1].status_code == 200
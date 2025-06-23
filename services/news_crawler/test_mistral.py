from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# 1. Настройка браузера
options = Options()
options.add_argument("--headless")  # без UI, если не нужно видеть
driver = webdriver.Chrome(options=options)

try:
    # 2. Открываем страницу с статьёй
    url = "https://www.pcgamer.com/games/adventure/dispatch-is-the-first-telltale-style-game-ive-played-thats-delivering-on-the-promise-of-playing-a-tv-show-and-its-even-got-a-compelling-management-sim-tucked-inside-too/"
    driver.get(url)

    # 3. Ждём, пока появится кнопка "Play"
    play_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "video-aspect-box"))
    )
    play_button.click()  # 4. Кликаем на "Play"

    # 5. Ждём немного, чтобы iframe успел подгрузиться
    time.sleep(5)

    # 6. Проверяем наличие iframe
    soup = BeautifulSoup(driver.page_source, "html.parser")
    iframe = soup.find("iframe")

    if iframe and iframe.has_attr("src"):
        print("👉 Iframe найден:", iframe.get_text())
    else:
        print("❗ Iframe не найден после клика")

finally:
    driver.quit()
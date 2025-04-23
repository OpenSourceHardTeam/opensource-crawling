import time
import requests
import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s [%(levelname)s] %(message)s'
)


def wait_for_selenium(timeout=20):
    selenium_url = os.getenv("SELENIUM_URL", "http://selenium:4444/wd/hub")
    print(f"Waiting for Selenium {selenium_url} ...", flush=True)
    for i in range(timeout):
        try:
            response = requests.get(selenium_url)
            if response.status_code == 200:
                print("Selenium is ready!")
                return
        except Exception as e:
            # logging.WARNING(f"connectionError : {e}")
            logging.warning(f"({i + 1}s) Connection error: {e}")
        time.sleep(1)
    raise RuntimeError("Selenium server did not become ready in time.")

def get_driver():
    mode = os.getenv("CRAWLER_MODE", "local")

    options = Options()
    options.add_argument("--headless")

    if mode == "docker":
        wait_for_selenium()
        # Docker에서는 selenium/standalone-chrome으로 접속
        driver = webdriver.Remote(
            command_executor= os.getenv("SELENIUM_URL", "http://selenium:4444/wd/hub"),
            options=options)
        driver.implicitly_wait(10)
        return driver
    else:
        # 로컬에서는 직접 chromedriver 사용
        return webdriver.Chrome(
            service=Service("/opt/homebrew/bin/chromedriver"),
            options=options
        )


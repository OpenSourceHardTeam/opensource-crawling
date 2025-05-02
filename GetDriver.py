import time
from selenium.common.exceptions import WebDriverException
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
    print(f"📡 Connecting to WebDriver at {selenium_url}", flush=True)

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    for i in range(20):
        try:
            driver = webdriver.Remote(
                command_executor=selenium_url,
                options=options
            )
            driver.get("https://www.google.com")
            print("✅ WebDriver 연결 성공", flush=True)
            return driver
        except WebDriverException as e:
            print(f"[{i + 1}s] WebDriver 연결 실패: {e}", flush=True)
            time.sleep(1)
        except Exception as e:
            print(f"[{i + 1}s] ❌ 알 수 없는 에러 발생: {e}", flush=True)
            time.sleep(1)

    raise RuntimeError("WebDriver를 20초 동안 연결하지 못했습니다.")

def get_driver():
    mode = os.getenv("CRAWLER_MODE", "local")

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    if mode == "docker":
        # Docker에서는 selenium/standalone-chrome으로 접속
        return wait_for_selenium()
    else:
        # 로컬에서는 직접 chromedriver 사용
        return webdriver.Chrome(
            service=Service("/opt/homebrew/bin/chromedriver"),
            options=options
        )


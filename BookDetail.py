import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_publisher_review(book_id, driver):
    # 책 상세 페이지
    base_url = "https://product.kyobobook.co.kr/detail/"
    url = base_url + book_id
    driver.get(url)

    time.sleep(1)

    try:
        # 탭 버튼이 존재할 때만 클릭 시도
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@id='scrollSpyProdInfo']//div[contains(@class, 'book_publish_review')]"))
        )
        # 버튼 클릭
        try:
            tab_button = driver.find_element(By.XPATH,
                                             "//*[@id='scrollSpyProdInfo']//div[contains(@class, 'book_publish_review')]//button")
            driver.execute_script("arguments[0].click();", tab_button)
            time.sleep(1)
        except:
            pass  # 클릭할 버튼이 없어도 무시

        # 실제 서평 텍스트 추출
        review_elem = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#scrollSpyProdInfo div.book_publish_review p"))
        )
        return review_elem.text.strip()

    except Exception:
        return None

import time
import schedule
from GetDriver import get_driver
from BookList import fetch_books_with_filter
from SaveBook import save_book

def crawler():
    try:
        print("크롤러 시작")

        driver = get_driver()
        print("드라이버 생성 완료")

        books = fetch_books_with_filter(driver)
        print(f"책 {len(books)}권 수집됨")

        save_book(books)
        driver.quit()
        print("크롤링 종료")
    except Exception as e:
        print(f"크롤러 에러 발생: {e}", flush=True)

# 매주 목요일 오후 3시에 실행
schedule.every().thursday.at("15:00").do(crawler)

print("스케줄러 실행 중 (Ctrl+C 종료)")
while True:
    schedule.run_pending()
    time.sleep(60)


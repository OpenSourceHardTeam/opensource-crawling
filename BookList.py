import http.client
import json
from BookDetail import get_publisher_review

# 제외시킬 카테고리
EXCLUDE_CATEGORIES = {"유아", "만화", "수험서/자격증", "어린이", "외국어", "어린이(초등)"}

def build_book_data(book, driver):
    print("처리 중:", book.get("cmdtName", "제목없음"))
    try:
        review = get_publisher_review(book.get("saleCmdtid"), driver)
    except Exception as e:
        print(f"서평 크롤링 실패: {e}")
        review = ""

    return {
        "book_cmdt_code": book.get("cmdtCode"),
        "book_rank": book.get("prstRnkn"),
        "book_image_url": f"https://contents.kyobobook.co.kr/sih/fit-in/200x0/pdt/{book.get('cmdtCode')}.jpg",
        "book_title": book.get("cmdtName", ""),
        "book_author": book.get("chrcName", ""),
        "book_description": book.get("inbukCntt", ""),
        "publisher_name": book.get("pbcmName", ""),
        "publish_date": book.get("rlseDate", ""),
        "publisher_review": review
    }

def fetch_books_with_filter(driver, limit=50):
    all_books = []
    page = 1

    while len(all_books) < limit:
        conn = http.client.HTTPSConnection("store.kyobobook.co.kr")
        conn.request(
            "GET",
            f"/api/gw/best/best-seller/total?page={page}&per=50&period=002&bsslBksClstCode=A",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        json_data = json.loads(data)

        best_sellers = json_data["data"]["bestSeller"]
        for book in best_sellers:
            category = book.get("saleCmdtClstName", "")
            if category in EXCLUDE_CATEGORIES:
                continue

            book_data = build_book_data(book, driver)

            all_books.append(book_data)
            if len(all_books) >= limit:
                break

        page += 1

    return all_books


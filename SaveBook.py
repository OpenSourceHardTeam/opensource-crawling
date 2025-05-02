import pymysql
import os
from dotenv import load_dotenv

load_dotenv(".env")

# DB 접속 정보 (본인 환경에 맞게 수정)
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),  # MySQL 사용자
    'password': os.getenv('DB_PASS'),  # MySQL 비밀번호
    'db': os.getenv('DB_NAME'),  # Spring Boot 쪽에서 만든 DB 이름
    'charset': 'utf8mb4'
}

def save_book(books):
    conn = pymysql.connect(**db_config)
    try:
        with conn.cursor() as cursor:
            # 1. book_cmdt_code 리스트 추출
            book_codes = [book['book_cmdt_code'] for book in books]

            # 2. 현재 있는 책 중에 삭제 대상 제거
            if book_codes:
                format_strings = ','.join(['%s'] * len(book_codes))
                delete_sql = f"""
                                DELETE FROM book_entity
                                WHERE book_cmdt_code NOT IN ({format_strings})
                            """
                cursor.execute(delete_sql, book_codes)

            # 3. insert or update
            insert_sql = """
                            INSERT INTO book_entity (
                                book_cmdt_code,
                                book_rank,
                                book_image_url,
                                book_title,
                                book_author,
                                book_description,
                                publisher_name,
                                publish_date,
                                publisher_review
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE
                                book_rank = VALUES(book_rank)
                        """

            for book in books:
                cursor.execute(insert_sql, (
                    book["book_cmdt_code"],
                    book["book_rank"],
                    book["book_image_url"],
                    book["book_title"],
                    book["book_author"],
                    book["book_description"],
                    book["publisher_name"],
                    book["publish_date"],
                    book["publisher_review"]
                ))

        conn.commit()
        print(f"✅ {len(books)}권 저장 완료 / 이전 책 삭제 완료", flush=True)
    except Exception as e:
        conn.rollback()
        print("❌ DB 동기화 실패:", e)
    finally:
        conn.close()


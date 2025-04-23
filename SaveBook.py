import pymysql
import os
from dotenv import load_dotenv

load_dotenv(".env.local")

# DB 접속 정보 (본인 환경에 맞게 수정)
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),  # MySQL 사용자
    'password': os.getenv('DB_PASS'),  # MySQL 비밀번호
    'db': os.getenv('DB_NAME'),  # Spring Boot 쪽에서 만든 DB 이름
    'charset': 'utf8mb4'
}

def save_book(book):
    conn = pymysql.connect(**db_config)
    try:
        with conn.cursor() as cursor:
            sql = """
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
            cursor.execute(sql, (
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
        print("저장 성공:", book["book_title"])
    except Exception as e:
        conn.rollback()
        print("저장 실패:", e)
    finally:
        conn.close()


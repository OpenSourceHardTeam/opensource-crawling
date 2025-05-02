FROM python:3.9-slim

# 시스템 패키지 설치
RUN apt-get update && \
    apt-get install -y gcc libffi-dev libssl-dev curl && \
    apt-get clean

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 복사 및 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 코드 복사
COPY . .

# 실행 명령
CMD ["python", "-u", "crawler.py"]


import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# SMTP 설정
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
EMAIL_USER = os.getenv("EMAIL_USER", "")
EMAIL_PASS = os.getenv("EMAIL_PASS", "")

# Kakao
KAKAO_TOKEN        = os.getenv("KAKAO_TOKEN", "")         # 내톡(카카오톡 일반 봇)

# JSON 파일
KEYWORD_FILE        = os.getenv("KEYWORD_FILE", "keywords.json")
EMAIL_FILE          = os.getenv("EMAIL_FILE", "emails.json")
KAKAO_WEBHOOKS_FILE = os.getenv("KAKAO_WEBHOOKS_FILE", "kakao_webhooks.json")

# 스케줄/크롤링 기본값
TIMEZONE     = os.getenv("TIMEZONE", "Asia/Seoul")
MAX_ARTICLES = int(os.getenv("MAX_ARTICLES", 50))

BASE_DIR      = os.path.dirname(os.path.dirname(__file__))
FEED_SPEC_CSV = os.path.join(BASE_DIR, "data", "rss.csv")

# RSS 피드 요청 타임아웃: (connect_timeout, read_timeout)
FEED_TIMEOUT    = (3, 10)
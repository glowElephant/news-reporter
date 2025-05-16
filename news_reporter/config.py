import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# SMTP 설정
SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
EMAIL_USER = os.getenv("EMAIL_USER", "")
EMAIL_PASS = os.getenv("EMAIL_PASS", "")

# Kakao
KAKAO_TOKEN        = os.getenv("KAKAO_TOKEN", "")         # 내톡(카카오톡 일반 봇)
KAKAO_WORK_WEBHOOK = os.getenv("KAKAO_WORK_WEBHOOK", "")   # 카카오워크 Webhook URL (콤마로 여러 개 가능)

# JSON 파일
KEYWORD_FILE        = os.getenv("KEYWORD_FILE", "keywords.json")
EMAIL_FILE          = os.getenv("EMAIL_FILE", "emails.json")
KAKAO_WEBHOOKS_FILE = os.getenv("KAKAO_WEBHOOKS_FILE", "kakao_webhooks.json")

# 스케줄/크롤링 기본값
TIMEZONE     = os.getenv("TIMEZONE", "Asia/Seoul")
MAX_ARTICLES = int(os.getenv("MAX_ARTICLES", 5))
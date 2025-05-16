# news_reporter/notifier.py

import json
import requests
import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import pytz
from datetime import datetime

import news_reporter.config as cfg   # config 모듈 전체를 import

def send_email(html_body: str, recipients: list[str]):
    tz = pytz.timezone(cfg.TIMEZONE)
    msg = MIMEText(html_body, "html")
    msg["Subject"] = f"Daily News Report - {datetime.now(tz):%Y-%m-%d}"
    msg["From"]    = cfg.EMAIL_USER
    msg["To"]      = ", ".join(recipients)
    with smtplib.SMTP_SSL(cfg.SMTP_HOST, cfg.SMTP_PORT) as smtp:
        smtp.login(cfg.EMAIL_USER, cfg.EMAIL_PASS)
        smtp.send_message(msg)

def send_kakaowork_message(text: str, webhook_url: str):
    if not webhook_url:
        return
    requests.post(webhook_url, json={"text": text})

def send_kakao_default(text: str):
    # 여기서 cfg.KAKAO_TOKEN을 참조하도록 변경
    if not cfg.KAKAO_TOKEN:
        return
    headers = {"Authorization": f"Bearer {cfg.KAKAO_TOKEN}"}
    template_obj = {
        "object_type": "text",
        "text": text,
        "link": {"web_url": "", "mobile_web_url": ""}
    }
    requests.post(
        "https://kapi.kakao.com/v2/api/talk/memo/default/send",
        headers=headers,
        data={"template_object": json.dumps(template_obj)}
    )

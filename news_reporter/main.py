# news_reporter/main.py

import pytz
from datetime import datetime
from bs4 import BeautifulSoup

from .config   import KEYWORD_FILE, EMAIL_FILE, KAKAO_WEBHOOKS_FILE, TIMEZONE
from .utils    import load_json
from .crawler  import fetch_from_rss
from .notifier import send_email, send_kakaowork_message, send_kakao_default

def fetch_and_send():
    """
    1) 키워드 JSON에서 불러오기
    2) RSS 피드에서 키워드별 기사 수집(fetch_from_rss)
    3) 이메일/카카오톡으로 발송
    """
    # 1) 설정 파일에서 키워드 · 이메일 · 웹훅 리스트 로드
    keywords = load_json(KEYWORD_FILE)
    emails   = load_json(EMAIL_FILE)
    hooks    = load_json(KAKAO_WEBHOOKS_FILE)

    # 키워드나 발송 대상이 없으면 종료
    if not keywords or not (emails or hooks):
        return

    # 2) RSS에서 기사 수집
    all_articles = []
    for kw in keywords:
        all_articles += fetch_from_rss(kw)

    # 수집된 기사가 없으면 종료
    if not all_articles:
        return

    # 3) HTML 본문 조립
    tz       = pytz.timezone(TIMEZONE)
    date_str = datetime.now(tz).strftime('%Y-%m-%d')
    html = f"<h2>🗞️ Daily News Report - {date_str}</h2>"
    for kw, title, link in all_articles:
        html += (
            f"<p>🔍 <strong>{kw}</strong>: "
            f"<a href='{link}' target='_blank'>{title}</a></p>"
        )

    # 4) 이메일 발송 (리스트가 비어있지 않을 때)
    if emails:
        send_email(html, emails)

    # 5) 카카오 메시지용 텍스트로 변환
    text = BeautifulSoup(html, 'html.parser').get_text(separator='\n')

    # 6) KakaoWork Webhook 발송
    for hook in hooks:
        send_kakaowork_message(text, hook)
    # 7) 일반 카카오톡(내톡) 발송
    send_kakao_default(text)

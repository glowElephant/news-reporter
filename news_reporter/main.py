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
    1) 키워드 · 이메일 · 웹훅 로드
    2) RSS에서 키워드별 기사 수집
    3) 이메일/카카오워크로 발송
    """
    # 1) 설정 로드
    keywords = load_json(KEYWORD_FILE)
    emails   = load_json(EMAIL_FILE)
    hooks    = load_json(KAKAO_WEBHOOKS_FILE)
    print(f"[MAIN] load_json → 키워드={keywords}, 이메일수신자={emails}, 웹훅={hooks}")

    # 발송 대상 없으면 종료
    if not keywords or not emails:
        print("[MAIN][WARN] 키워드 또는 이메일 수신자 없음, 중단")
        return

    # 2) RSS 크롤링
    all_articles = []
    for kw in keywords:
        print(f"[MAIN] ▶▶▶ 키워드 '{kw}' 크롤링 시작")
        arts = fetch_from_rss(kw)
        all_articles += arts
        print(f"[MAIN] ◀◀◀ 키워드 '{kw}' 완료 — 누적 기사수: {len(all_articles)}")

    if not all_articles:
        print("[MAIN][WARN] 수집된 기사 없음, 중단")
        return

    print(f"[MAIN] 총 수집된 기사: {len(all_articles)}건 → 이메일 발송 준비")

    # 3) HTML 본문 조립
    tz       = pytz.timezone(TIMEZONE)
    date_str = datetime.now(tz).strftime('%Y-%m-%d')
    html = f"<h2>🗞️ Daily News Report - {date_str}</h2>"
    for kw, title, link in all_articles:
        html += f"<p>🔍 <strong>{kw}</strong>: <a href='{link}' target='_blank'>{title}</a></p>"

    # 4) 이메일 발송
    send_email(html, emails)

    # (선택) 카카오워크 발송
    if hooks:
        text = BeautifulSoup(html, 'html.parser').get_text(separator='\n')
        for hook in hooks:
            send_kakaowork_message(text, hook)

    # (내톡 제외)
    print("[MAIN] fetch_and_send 완료\n")

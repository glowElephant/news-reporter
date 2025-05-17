# news_reporter/crawler.py

import requests
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from datetime import datetime, timedelta, time
import pytz

from .config import MAX_ARTICLES, TIMEZONE, FEED_TIMEOUT

def fetch_from_rss(keyword: str) -> list[tuple[str, str, str]]:
    """
    어제 09:01부터 현재 시각까지 발행된 기사 중에서
    키워드에 매칭된 최신 기사를 최대 MAX_ARTICLES개수만큼 반환합니다.
    반환 형식: [(keyword, title, link), ...]
    """
    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)
    # 기준 윈도우: 어제 09:01
    yesterday = now.date() - timedelta(days=1)
    start_dt = tz.localize(datetime.combine(yesterday, time(9, 1)))

    print(f"[CRAWLER] 시작: 키워드='{keyword}'  윈도우 {start_dt} 부터 {now} 까지  최대={MAX_ARTICLES}")
    results = []

    for source_name, feed_url in RSS_FEEDS:
        print(f"[CRAWLER] RSS 요청 → {source_name}: {feed_url}")
        try:
            resp = requests.get(feed_url, timeout=FEED_TIMEOUT)
            resp.raise_for_status()
            root = ET.fromstring(resp.content)

            feed_count = 0
            for item in root.findall(".//item"):
                # 1) pubDate 파싱
                pub_txt = item.findtext("pubDate", "")
                if not pub_txt:
                    continue
                pub_dt = parsedate_to_datetime(pub_txt)
                if pub_dt.tzinfo is None:
                    pub_dt = tz.localize(pub_dt)
                else:
                    pub_dt = pub_dt.astimezone(tz)

                # 2) 윈도우 필터링
                if not (start_dt <= pub_dt <= now):
                    continue

                # 3) 키워드 매칭
                title = item.findtext("title", "") or ""
                link  = item.findtext("link", "") or ""
                desc  = item.findtext("description", "") or ""
                if keyword in title or keyword in desc:
                    results.append((keyword, title, link))
                    feed_count += 1

                if len(results) >= MAX_ARTICLES:
                    break

            print(f"[CRAWLER] {source_name}에서 윈도우 내 매칭 기사: {feed_count}건  (누적: {len(results)})")

        except Exception as e:
            print(f"[CRRAWLER][ERROR] {source_name} 요청/파싱 오류:", e)
            continue

        if len(results) >= MAX_ARTICLES:
            break

    print(f"[CRAWLER] 완료: 총 {len(results)}건 수집\n")
    return results

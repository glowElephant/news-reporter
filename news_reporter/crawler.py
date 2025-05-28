# news_reporter/crawler.py

import requests
import xml.etree.ElementTree as ET
import csv
from email.utils import parsedate_to_datetime
from datetime import datetime, timedelta, time
import pytz

from .config import MAX_ARTICLES, TIMEZONE, FEED_TIMEOUT, FEED_SPEC_CSV

def load_feed_specs() -> list[tuple[str, str]]:
    """
    data/feed_spec.csv를 읽어 [(name, url), ...] 리스트로 반환합니다.
    - CSV 헤더는 반드시 'name'과 'url' 컬럼을 포함해야 합니다.
    """
    feeds = []
    try:
        with open(FEED_SPEC_CSV, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row["name"]   # CSV 헤더에 'name' 컬럼이 있는지 꼭 확인!
                url  = row["url"]
                feeds.append((name, url))
    except FileNotFoundError:
        print(f"[CRAWLER][ERROR] 피드 스펙 파일을 찾을 수 없습니다: {FEED_SPEC_CSV}")
    except KeyError as e:
        print(f"[CRAWLER][ERROR] feed_spec.csv 헤더에 컬럼이 없습니다: {e}")
    return feeds

# CSV를 로드해서 전역 변수로 저장 (import 시 한 번만 실행)
RSS_FEEDS = load_feed_specs()

def fetch_from_rss(keyword: str) -> list[tuple[str, str, str]]:
    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)
    # 어제 09:01부터 지금까지 창
    yesterday = now.date() - timedelta(days=1)
    start_dt = tz.localize(datetime.combine(yesterday, time(9, 1)))

    print(f"[CRAWLER] 시작: 키워드='{keyword}'  윈도우: {start_dt} ~ {now}  MAX={MAX_ARTICLES}")
    results = []

    # **RSS_FEEDS가 비어있다면 여기서 에러가 납니다.**
    if not RSS_FEEDS:
        print("[CRRAWLER][WARN] RSS_FEEDS 리스트가 비어 있습니다. feed_spec.csv를 확인하세요.")
        return results

    for source_name, feed_url in RSS_FEEDS:
        print(f"[CRAWLER] RSS 요청 → {source_name}: {feed_url}")
        try:
            resp = requests.get(feed_url, timeout=FEED_TIMEOUT)
            resp.raise_for_status()
            root = ET.fromstring(resp.content)

            feed_count = 0
            for item in root.findall(".//item"):
                # pubDate 파싱
                pub_txt = item.findtext("pubDate", "")
                if not pub_txt:
                    continue
                pub_dt = parsedate_to_datetime(pub_txt)
                pub_dt = pub_dt.astimezone(tz) if pub_dt.tzinfo else tz.localize(pub_dt)

                # 시간 윈도우 필터
                if not (start_dt <= pub_dt <= now):
                    continue

                # 키워드 매칭
                title = item.findtext("title", "") or ""
                link  = item.findtext("link", "") or ""
                desc  = item.findtext("description", "") or ""
                if keyword in title or keyword in desc:
                    results.append((keyword, title, link))
                    feed_count += 1

                if len(results) >= MAX_ARTICLES:
                    break

            print(f"[CRAWLER] {source_name} 매칭 기사: {feed_count}건  (누적: {len(results)})")

        except Exception as e:
            print(f"[CRAWLER][ERROR] {source_name} 요청/파싱 오류:", e)
            continue

        if len(results) >= MAX_ARTICLES:
            break

    print(f"[CRAWLER] 완료: 총 {len(results)}건 수집\n")
    return results

import requests
import xml.etree.ElementTree as ET
import csv

from .config import MAX_ARTICLES, FEED_SPEC_CSV

def load_feed_specs() -> list[tuple[str, str]]:
    feeds = []
    with open(FEED_SPEC_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 헤더에 맞게 'name' 컬럼을 사용합니다
            name = row["name"]  
            url  = row["url"]
            feeds.append((name, url))
    return feeds

# CSV 로딩해서 전역 FEEDS로 사용
RSS_FEEDS = load_feed_specs()

def fetch_from_rss(keyword: str) -> list[tuple[str, str, str]]:
    results: list[tuple[str, str, str]] = []
    print(f"[CRAWLER] 시작: 키워드='{keyword}'  최대기사수={MAX_ARTICLES}")

    for source_name, feed_url in RSS_FEEDS:
        print(f"[CRAWLER] RSS 요청 → {source_name}: {feed_url}")
        try:
            resp = requests.get(feed_url, timeout=(3,10))
            resp.raise_for_status()
            root = ET.fromstring(resp.content)

            feed_count = 0
            for item in root.findall(".//item"):
                title = item.findtext("title", "") or ""
                link  = item.findtext("link", "") or ""
                desc  = item.findtext("description", "") or ""

                if keyword in title or keyword in desc:
                    results.append((keyword, title, link))
                    feed_count += 1

                if len(results) >= MAX_ARTICLES:
                    break

            print(f"[CRAWLER] {source_name}에서 매칭 기사: {feed_count}건  (누적: {len(results)})")

        except Exception as e:
            print(f"[CRAWLER][ERROR] {source_name} 요청/파싱 중 오류:", e)
            continue

        if len(results) >= MAX_ARTICLES:
            break

    print(f"[CRAWLER] 완료: 총 {len(results)}건 수집\n")
    return results

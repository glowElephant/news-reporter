# news_reporter/crawler.py

import requests
import xml.etree.ElementTree as ET
from .config import MAX_ARTICLES

# 1) 사용할 RSS 피드 목록 (필요시 추가/삭제)
RSS_FEEDS = [
    ("연합뉴스", "https://www.yna.co.kr/rss/all.xml"),
    ("조선일보", "http://rss.chosun.com/site/data/rss/rss.xml"),
    ("중앙일보", "https://rss.joins.com/joins_news_list.xml"),
    ("동아일보", "https://www.donga.com/news/rss"),
    # ("한겨레", "https://rss.hani.co.kr/rss/politics.xml"), 등
]

def fetch_from_rss(keyword: str) -> list[tuple[str, str, str]]:
    """
    RSS 피드에서 키워드를 포함한 최신 기사를 최대 MAX_ARTICLES개수만큼 가져옵니다.
    반환 형식: [(keyword, title, link), ...]
    """
    results: list[tuple[str, str, str]] = []

    for source_name, feed_url in RSS_FEEDS:
        try:
            resp = requests.get(feed_url, timeout=5)
            resp.raise_for_status()
            root = ET.fromstring(resp.content)

            # <item> 태그마다 검사
            for item in root.findall(".//item"):
                title = item.findtext("title", "") or ""
                link  = item.findtext("link", "") or ""
                desc  = item.findtext("description", "") or ""

                # 제목 또는 설명에 키워드가 포함됐으면 결과에 추가
                if keyword in title or keyword in desc:
                    results.append((keyword, title, link))

                # 최대 개수에 도달하면 브레이크
                if len(results) >= MAX_ARTICLES:
                    break

        except Exception:
            # 네트워크 오류나 XML 파싱 오류가 발생해도 다음 피드로 계속 진행
            continue

        # 이미 충분히 모였으면 더 이상 탐색 안 함
        if len(results) >= MAX_ARTICLES:
            break

    return results

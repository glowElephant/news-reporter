import pytest
from news_reporter.crawler import fetch_from_rss
from news_reporter.config import MAX_ARTICLES

class DummyResponse:
    def __init__(self, content):
        self.content = content
    def raise_for_status(self):
        pass


def test_fetch_from_rss(monkeypatch):
    keyword = "Python"
    sample_rss = f"""<?xml version=\"1.0\"?>
<rss>
  <channel>
    <item>
      <title>Learn {keyword} Programming</title>
      <link>http://example.com/1</link>
      <description>{keyword} basics tutorial</description>
    </item>
    <item>
      <title>Unrelated News</title>
      <link>http://example.com/2</link>
      <description>No match here</description>
    </item>
  </channel>
</rss>"""
    # requests.get이 DummyResponse 반환하도록 패치
    monkeypatch.setattr('requests.get', lambda url, timeout=None: DummyResponse(sample_rss.encode('utf-8')))

    results = fetch_from_rss(keyword)
    assert isinstance(results, list)
    assert results, "결과 리스트가 비어있습니다."
    # 첫 번째 결과가 키워드 포함 기사인지 확인
    assert results[0] == (keyword, f"Learn {keyword} Programming", "http://example.com/1")


def test_fetch_from_rss_respects_max_articles(monkeypatch):
    keyword = "Test"
    # MAX_ARTICLES+2개의 아이템 생성
    items_xml = ''
    for i in range(MAX_ARTICLES + 2):
        items_xml += f"""
        <item>
          <title>{keyword} Article {i}</title>
          <link>http://example.com/{i}</link>
          <description>Description with {keyword}</description>
        </item>"""
    sample_rss = f"<?xml version=\"1.0\"?><rss><channel>{items_xml}</channel></rss>"
    monkeypatch.setattr('requests.get', lambda url, timeout=None: DummyResponse(sample_rss.encode('utf-8')))

    results = fetch_from_rss(keyword)
    # MAX_ARTICLES 개수만큼 리턴
    assert len(results) == MAX_ARTICLES
    for idx, (_, title, link) in enumerate(results):
        assert title == f"{keyword} Article {idx}"
        assert link == f"http://example.com/{idx}"
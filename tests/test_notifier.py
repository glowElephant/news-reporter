import json
import pytest
from news_reporter.notifier import send_email, send_kakaowork_message, send_kakao_default

# Dummy SMTP 클래스
class DummySMTP:
    def __init__(self):
        self.sent = []
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        pass
    def login(self, user, passwd):
        pass
    def send_message(self, msg):
        self.sent.append(msg)


def test_send_email(monkeypatch):
    instance = {}
    def dummy_smtp(host, port):
        inst = DummySMTP()
        instance['smtp'] = inst
        return inst
    monkeypatch.setattr('news_reporter.notifier.smtplib.SMTP_SSL', dummy_smtp)

    html = "<h1>Hello</h1>"
    recipients = ["a@b.com"]
    send_email(html, recipients)

    assert 'smtp' in instance
    sent = instance['smtp'].sent
    assert len(sent) == 1
    msg = sent[0]
    assert '<h1>Hello</h1>' in msg.get_payload()


def test_send_kakaowork_message(monkeypatch):
    called = {}
    def dummy_post(url, json=None):
        called['url'] = url
        called['json'] = json
    monkeypatch.setattr('requests.post', dummy_post)

    text = "Hello KakaoWork"
    send_kakaowork_message(text, "http://hook.url")
    assert called['url'] == "http://hook.url"
    assert called['json'] == {"text": text}


def test_send_kakao_default(monkeypatch):
    called = {}
    def dummy_post(url, headers=None, data=None):
        called['url'] = url
        called['headers'] = headers
        called['data'] = data
    monkeypatch.setattr('requests.post', dummy_post)

    # 테스트용 토큰 설정
    import news_reporter.config as cfg
    cfg.KAKAO_TOKEN = "dummy_token"

    text = "Hello Kakao"
    send_kakao_default(text)

    assert called['url'] == "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    assert 'Bearer dummy_token' in called['headers']['Authorization']
    obj = json.loads(called['data']['template_object'])
    assert obj['text'] == text

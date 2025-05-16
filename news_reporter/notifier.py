# news_reporter/notifier.py

import json
import requests
import smtplib
from email.mime.text import MIMEText
import pytz
from datetime import datetime
import time
import pyautogui

import news_reporter.config as cfg
from news_reporter.utils import load_json

# ---- Email & KakaoWork & KakaoMemo Functions ----

def send_email(html_body: str, recipients: list[str]):
    """
    HTML 메일을 SMTP를 통해 발송합니다.
    """
    print(f"[NOTIFIER] send_email 호출 → recipients: {recipients}")
    try:
        tz = pytz.timezone(cfg.TIMEZONE)
        msg = MIMEText(html_body, "html")
        msg["Subject"] = f"Daily News Report - {datetime.now(tz):%Y-%m-%d}"
        msg["From"]    = cfg.EMAIL_USER
        msg["To"]      = ", ".join(recipients)

        with smtplib.SMTP_SSL(cfg.SMTP_HOST, cfg.SMTP_PORT) as smtp:
            smtp.login(cfg.EMAIL_USER, cfg.EMAIL_PASS)
            smtp.send_message(msg)
        print("[NOTIFIER] send_email 성공")
    except Exception as e:
        print(f"[NOTIFIER][ERROR] send_email 실패: {e}")


def send_kakaowork_message(text: str, webhook_url: str):
    """
    KakaoWork Incoming Webhook URL로 텍스트 메시지를 발송합니다.
    """
    print(f"[NOTIFIER] send_kakaowork_message 호출 → webhook: {webhook_url}")
    try:
        resp = requests.post(webhook_url, json={"text": text}, timeout=5)
        print(f"[NOTIFIER] 카카오워크 응답: {resp.status_code} / {resp.text}")
    except Exception as e:
        print(f"[NOTIFIER][ERROR] send_kakaowork_message 실패: {e}")


def send_kakao_default(text: str):
    """
    카카오톡 '내게 보내기'(메모) API로 메시지를 발송합니다.
    """
    print(f"[NOTIFIER] send_kakao_default 호출 → token 길이: {len(cfg.KAKAO_TOKEN)}")
    if not cfg.KAKAO_TOKEN:
        print("[NOTIFIER][WARN] KAKAO_TOKEN 미설정, 일반카톡 발송 건너뜀")
        return

    headers = {"Authorization": f"Bearer {cfg.KAKAO_TOKEN}"}
    template_obj = {
        "object_type": "text",
        "text": text,
        "link": {"web_url": "", "mobile_web_url": ""}
    }

    try:
        resp = requests.post(
            "https://kapi.kakao.com/v2/api/talk/memo/default/send",
            headers=headers,
            data={"template_object": json.dumps(template_obj)},
            timeout=5
        )
        print(f"[NOTIFIER] 일반 카카오톡 응답: {resp.status_code} / {resp.text}")
    except Exception as e:
        print(f"[NOTIFIER][ERROR] send_kakao_default 실패: {e}")

# ---- PC KakaoTalk GUI 자동화 함수 ----

def send_kakao_gui(text: str, room_name: str):
    """
    PC 카카오톡 앱을 UI 자동화로 조작해 지정된 채팅방에 메시지 보냅니다.
    room_name: 채팅방 검색창에 입력할 문자열
    """
    print(f"[GUI] send_kakao_gui 호출 → room: {room_name}")
    # 1) 카카오톡 아이콘 클릭해 창 활성화
    icon = pyautogui.locateCenterOnScreen('assets/kao_icon.png', confidence=0.8)
    if not icon:
        print("[GUI][ERROR] 카카오톡 아이콘을 찾을 수 없습니다.")
        return
    pyautogui.click(icon)
    time.sleep(0.5)

    # 2) 검색창 클릭 → 방 이름 입력 → Enter
    search = pyautogui.locateCenterOnScreen('assets/search_box.png', confidence=0.8)
    if not search:
        print("[GUI][ERROR] 검색창 아이콘을 찾을 수 없습니다.")
        return
    pyautogui.click(search)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.typewrite(room_name, interval=0.05)
    pyautogui.press('enter')
    time.sleep(0.5)

    # 3) 메시지 입력창 클릭 → 메시지 입력 → Enter
    msg_box = pyautogui.locateCenterOnScreen('assets/message_box.png', confidence=0.8)
    if not msg_box:
        print("[GUI][ERROR] 메시지 입력창을 찾을 수 없습니다.")
        return
    pyautogui.click(msg_box)
    pyautogui.typewrite(text, interval=0.01)
    pyautogui.press('enter')
    print(f"[GUI] '{room_name}' 방에 메시지 전송 완료.")


def send_kakao_gui_all(text: str):
    """
    json 파일(gui_rooms.json)에서 방 이름 리스트를 불러와서
    send_kakao_gui를 통해 모두 메시지 전송합니다.
    """
    rooms = load_json('gui_rooms.json')
    print(f"[GUI] send_kakao_gui_all 호출 → rooms: {rooms}")
    for room in rooms:
        send_kakao_gui(text, room)

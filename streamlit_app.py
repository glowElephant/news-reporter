import streamlit as st
import re

from news_reporter.scheduler import start_scheduler
from news_reporter.main import fetch_and_send
from news_reporter.utils import load_json, save_json
from news_reporter.config import KEYWORD_FILE, EMAIL_FILE, KAKAO_WEBHOOKS_FILE

# ──────────────────────────────────────────────────────────────────────────────
# 1) 스케줄러 (BackgroundScheduler) 시작
# ──────────────────────────────────────────────────────────────────────────────
if 'scheduler_started' not in st.session_state:
    start_scheduler()
    st.session_state.scheduler_started = True

# ──────────────────────────────────────────────────────────────────────────────
# 2) Streamlit UI 설정
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="🗞️ Daily News Report Manager", layout="centered")
st.title("🗞️ Daily News Report Manager")

# --- 1. Keywords 관리 ---
st.subheader("1. Keywords")
keywords = load_json(KEYWORD_FILE)
for kw in keywords:
    col1, col2 = st.columns([4, 1])
    col1.write(kw)
    if col2.button("Delete", key=f"del_kw_{kw}"):
        keywords.remove(kw)
        save_json(KEYWORD_FILE, keywords)
        st.experimental_rerun()

new_kw = st.text_input("Add new keyword", key="add_kw")
if st.button("Add Keyword"):
    if new_kw.strip():
        keywords.append(new_kw.strip())
        save_json(KEYWORD_FILE, keywords)
        st.experimental_rerun()
    else:
        st.warning("키워드를 입력해주세요.")

# --- 2. Email Recipients 관리 ---
st.subheader("2. Email Recipients")
emails = load_json(EMAIL_FILE)
for addr in emails:
    col1, col2 = st.columns([4, 1])
    col1.write(addr)
    if col2.button("Delete", key=f"del_email_{addr}"):
        emails.remove(addr)
        save_json(EMAIL_FILE, emails)
        st.experimental_rerun()

new_email = st.text_input("Add new email", key="add_email")
if st.button("Add Email"):
    if re.match(r"[^@]+@[^@]+\.[^@]+", new_email):
        emails.append(new_email)
        save_json(EMAIL_FILE, emails)
        st.experimental_rerun()
    else:
        st.error("유효한 이메일 형식이 아닙니다.")

# --- 3. KakaoWork Webhook 관리 ---
st.subheader("3. KakaoWork Webhooks")
webhooks = load_json(KAKAO_WEBHOOKS_FILE)
for hook in webhooks:
    col1, col2 = st.columns([4, 1])
    col1.write(hook)
    if col2.button("Delete", key=f"del_hook_{hook}"):
        webhooks.remove(hook)
        save_json(KAKAO_WEBHOOKS_FILE, webhooks)
        st.experimental_rerun()

new_hook = st.text_input("Add new webhook URL", key="add_hook")
if st.button("Add Webhook"):
    if new_hook.startswith("http"):
        webhooks.append(new_hook)
        save_json(KAKAO_WEBHOOKS_FILE, webhooks)
        st.experimental_rerun()
    else:
        st.error("유효한 URL 형식이 아닙니다.")

# --- 정보 메시지 ---
st.info(
    "Settings are persisted in JSON files:\n"
    f"- {KEYWORD_FILE}\n"
    f"- {EMAIL_FILE}\n"
    f"- {KAKAO_WEBHOOKS_FILE}"
)

# (선택) 수동 실행 버튼
if st.button("Send Now"):
    fetch_and_send()
    st.success("뉴스 리포트 발송이 완료되었습니다.")

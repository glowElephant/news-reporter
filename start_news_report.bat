@echo off
REM 1) 작업 디렉터리로 이동: 실제 경로로 수정하세요
cd /d C:\Git\news-reporter

REM 2) 가상환경 활성화 (venv를 쓰는 경우)
call C:\Git\news-reporter\venv\Scripts\activate.bat

REM 3) Streamlit 앱 백그라운드 실행
streamlit run streamlit_app.py --server.headless true

REM (옵션) 가상환경 비활성화
REM deactivate

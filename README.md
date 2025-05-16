# Daily News Reporter

Streamlit UI와 APScheduler 기반으로, 국내 주요 언론사의 RSS 피드에서 키워드별 최신 뉴스를 크롤링하여  
매일 오전 9시에 지정된 이메일로 리포트해 주는 도구입니다.

---

## 주요 기능

- **키워드 관리**  
  Streamlit UI에서 원하는 키워드를 추가·삭제  
- **이메일 수신자 관리**  
  Streamlit UI에서 수신자 이메일 주소를 추가·삭제  
- **RSS 피드 확장성**  
  `data/feed_spec.csv`에 매체·카테고리·URL 스펙만 추가하면 자동으로 크롤링 대상 확장  
- **자동 스케줄링**  
  앱 실행 시 APScheduler가 백그라운드에서 매일 오전 9시(Asia/Seoul) 발송  
- **수동 발송 버튼**  
  “Send Now” 버튼을 눌러 즉시 리포트 발송 가능  
- **단위 테스트**  
  `pytest` 기반 크롤러·노티파이어 테스트 포함  

---

## 디렉터리 구조

```
news-reporter/
├─ data/
│  └─ feed_spec.csv        # RSS 피드 스펙 (publisher,id,name,type,url)
├─ news_reporter/
│  ├─ __init__.py
│  ├─ config.py            # .env 로딩 및 설정
│  ├─ crawler.py           # CSV 기반 RSS 크롤러
│  ├─ main.py              # fetch_and_send() 구현
│  ├─ notifier.py          # send_email(), send_kakaowork_message() 등
│  ├─ scheduler.py         # APScheduler 설정
│  └─ utils.py             # JSON 파일 입출력
├─ tests/
│  ├─ __init__.py
│  ├─ test_crawler.py
│  └─ test_notifier.py
├─ streamlit_app.py        # Streamlit UI
├─ .env.example            # 환경변수 예시
├─ requirements.txt        # 의존 패키지
└─ README.md
```

---

## 시작하기 (Setup)

1. 저장소 클론  
   ```bash
   git clone https://github.com/<YOUR_USERNAME>/news-reporter.git
   cd news-reporter
   ```

2. 가상환경 생성 & 활성화  
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. 의존성 설치  
   ```bash
   pip install -r requirements.txt
   ```

4. 환경변수 설정  
   프로젝트 루트에 `.env` 파일을 생성하고, 아래 내용을 채웁니다:
   ```ini
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=465
   EMAIL_USER=your.address@gmail.com
   EMAIL_PASS=앱비밀번호_16자리
   TIMEZONE=Asia/Seoul
   MAX_ARTICLES=50
   ```

5. RSS 피드 스펙 확인  
   `data/feed_spec.csv` 에서 `<publisher>,<id>,<name>,<type>,<url>` 형식으로 관리  
   새로운 매체를 추가하려면 한 줄씩 스펙을 추가하고 저장하세요.

---

## 사용법

### Streamlit UI 실행
```bash
streamlit run streamlit_app.py
```
- 브라우저에서 키워드·이메일 수신자 관리, 수동 발송 가능

### 자동 스케줄링
- 앱을 실행해 두면 매일 오전 9시에 자동으로 리포트가 이메일로 발송됩니다.

### 테스트
```bash
pytest
```

---

## 환경설정

| 변수              | 설명                                      | 기본값            |
|------------------|-----------------------------------------|------------------|
| SMTP_HOST        | SMTP 서버 호스트                          | (필수)            |
| SMTP_PORT        | SMTP 포트                                 | 465              |
| EMAIL_USER       | 보내는 계정 이메일                        | (필수)            |
| EMAIL_PASS       | SMTP 로그인 비밀번호(앱 비밀번호 추천)       | (필수)            |
| TIMEZONE         | 크론 트리거 타임존                         | Asia/Seoul       |
| MAX_ARTICLES     | 키워드당 최대 수집 기사 개수               | 50               |

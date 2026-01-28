# Backend B - 투표/집계 API

서바이벌 프로그램 대중 투표 및 결과 집계 API

## 담당 기능

- 대중 투표 저장 (POST /polls/{id}/votes)
- 중복투표 방지 (IP + Fingerprint 기반)
- 결과 집계 (GET /polls/{id}/results)
- 패널 vs 대중 비교 분석

## 기술 스택

- Python 3.11+
- FastAPI
- MySQL
- SQLAlchemy

## 설치 및 실행

### 1. 가상환경 설정

```bash
cd backend-b
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 환경변수 설정

```bash
cp .env.example .env
# .env 파일 수정
```

### 4. DB 설정

```bash
mysql -u root -p < schema.sql
```

### 5. 서버 실행

```bash
# 개발 모드
uvicorn app.main:app --reload --port 8000

# 또는
python -m app.main
```

### 6. API 문서 확인

- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 엔드포인트

### 투표하기

```
POST /api/v1/polls/{poll_id}/votes

Headers:
  X-Fingerprint: <browser-fingerprint>

Body:
{
    "choice": "A셰프"
}

Response 201:
{
    "success": true,
    "message": "투표가 완료되었습니다",
    "data": {
        "poll_id": 1,
        "choice": "A셰프",
        "voted_at": "2025-01-27T10:30:00"
    }
}
```

### 결과 조회

```
GET /api/v1/polls/{poll_id}/results

Response 200:
{
    "success": true,
    "data": {
        "poll_id": 1,
        "title": "A셰프 vs B셰프",
        "public_votes": {
            "total": 100,
            "results": {
                "A셰프": { "count": 35, "percent": 35.0 },
                "B셰프": { "count": 65, "percent": 65.0 }
            }
        },
        "panel_result": {
            "A셰프": 70,
            "B셰프": 30
        },
        "comparison": {
            "biggest_gap": {
                "option": "A셰프",
                "panel_percent": 70,
                "public_percent": 35,
                "gap": 35
            },
            "public_favorite": "B셰프",
            "panel_favorite": "A셰프",
            "opinion_match": false
        }
    }
}
```

## 테스트

```bash
pytest tests/ -v
```

## 프로젝트 구조

```
backend-b/
├── app/
│   ├── main.py           # FastAPI 앱
│   ├── config.py         # 환경변수
│   ├── database.py       # DB 연결
│   ├── models/           # SQLAlchemy 모델
│   ├── schemas/          # Pydantic 스키마
│   ├── api/              # API 라우터
│   ├── services/         # 비즈니스 로직
│   └── utils/            # 유틸리티
├── tests/                # 테스트
├── requirements.txt
├── schema.sql            # DB 스키마
└── .env.example
```

## 중복투표 방지 정책

```
voter_id = SHA256(IP + Fingerprint + poll_id)
```

- 같은 IP + 같은 브라우저에서 같은 투표에 1회만 가능
- Rate Limit: IP당 분당 10회

# Text-to-Speech (TTS) 텍스트 음성 변환

FastAPI + Microsoft Edge TTS 기반의 텍스트 음성 변환 애플리케이션입니다. 텍스트 입력, 파일 업로드, 다양한 음성 선택 및 MP3 다운로드를 지원합니다.

## 빠른 시작

```bash
# 프로젝트 클론
git clone https://github.com/bob60bob123/tts-text2speech.git
cd tts-text2speech

# 의존성 설치
pip install -r requirements.txt

# 서버 시작
start.bat 더블클릭 또는:
uvicorn app.main:app --host 0.0.0.0 --port 8000

# 브라우저에서 열기
# http://127.0.0.1:8000
```

## 기능

- **텍스트 입력**: 텍스트를 직접 붙여넣어 변환
- **파일 업로드**: TXT, PDF, DOCX, MD 형식 지원
- **다양한 음성**: 11가지 신경망 음성 (중국어 + 영어)
- **재생 제어**: 재생/일시정지, 진행률 드래그, 속도 조절 (0.5x - 2.0x)
- **MP3 저장**: 변환 후音频 파일 저장

## 음성 목록

| 음성 ID                | 설명              |
| -------------------- | --------------- |
| zh-CN-XiaoxiaoNeural | 샤오샤오 (여성-청년) |
| zh-CN-XiaoyiNeural   | 샤오이 (여성-아동)   |
| zh-CN-YunxiaNeural   |윈샤 (여성-청년)    |
| zh-CN-YunxiNeural    | 윈시 (남성-청년)    |
| zh-CN-YunyangNeural  | 윈양 (남성-중년)    |
| zh-CN-YunjianNeural  | 윈젠 (남성-청년)    |
| en-US-AriaNeural     | Aria (여성-미국)   |
| en-US-GuyNeural      | Guy (남성-미국)    |
| en-US-JennyNeural    | Jenny (여성-미국)  |
| en-GB-SoniaNeural    | Sonia (여성-영국)  |
| en-GB-RyanNeural     | Ryan (남성-영국)   |

## 프로젝트 구조

```
app/
├── main.py              # FastAPI 진입점
├── api/
│   ├── routes.py        # API 라우팅
│   └── schemas.py       # Pydantic 모델
├── services/
│   ├── tts_service.py   # TTS 엔진 오케스트레이션
│   ├── file_parser.py   # 파일 파싱
│   └── audio_storage.py # 오디오 스토리지
└── engines/
    ├── base.py          # 엔진 추상 기본 클래스
    ├── edge_tts_engine.py   # Edge TTS (기본)
    ├── google_tts.py         # Google TTS
    └── pyttsx3_engine.py     # pyttsx3 (오프라인)

static/                  # 프론트엔드 리소스
├── index.html
├── css/styles.css
└── js/
    ├── api-client.js
    ├── app.js
    ├── audio-player.js  # 오디오 재생 + 진행률 드래그
    └── file-handler.js
```

## 기술 스택

- **프론트엔드**: Vanilla JS/CSS (프레임워크 없음)
- **백엔드**: FastAPI + Python 3.11+
- **TTS 엔진**: edge-tts, gtts, pyttsx3
- **파일 파싱**: PyPDF2, python-docx, mistune

## 엔진 우선순위

1. **Edge TTS** - 무료, 고품질, Microsoft 서버
2. **Google TTS** - 백업 옵션
3. **pyttsx3** - 완전 오프라인 (Windows 전용)

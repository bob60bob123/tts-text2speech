# Text-to-Speech (TTS) 文字转语音

基于 FastAPI + Microsoft Edge TTS 的文字转语音应用，支持粘贴文字、上传文件、多种音色选择和 MP3 下载。

## 快速开始

```bash
# 克隆项目
git clone https://github.com/bob60bob123/tts-text2speech.git
cd tts-text2speech

# 安装依赖
pip install -r requirements.txt

# 启动服务器
双击 start.bat 或运行:
uvicorn app.main:app --host 0.0.0.0 --port 8000

# 浏览器打开
# http://127.0.0.1:8000
```

## 功能特性

- **文本输入**: 直接粘贴文字进行转换
- **文件上传**: 支持 TXT、PDF、DOCX、MD 格式
- **多种音色**: 11 种神经网络音色（中文/英文）
- **播放控制**: 播放/暂停、进度拖动、速度调节 (0.5x - 2.0x)
- **MP3 保存**: 转换完成后可保存音频文件

## 音色列表

| 音色 ID                | 说明            |
| -------------------- | ------------- |
| zh-CN-XiaoxiaoNeural | 晓晓 (女声-年轻)    |
| zh-CN-XiaoyiNeural   | 小艺 (女声-童年)    |
| zh-CN-YunxiaNeural   | 云夏 (女声-年轻)    |
| zh-CN-YunxiNeural    | 云希 (男声-年轻)    |
| zh-CN-YunyangNeural  | 云扬 (男声-中年)    |
| zh-CN-YunjianNeural  | 云健 (男声-年轻)    |
| en-US-AriaNeural     | Aria (女声-美式)  |
| en-US-GuyNeural      | Guy (男声-美式)   |
| en-US-JennyNeural    | Jenny (女声-美式) |
| en-GB-SoniaNeural    | Sonia (女声-英式) |
| en-GB-RyanNeural     | Ryan (男声-英式)  |

## 项目结构

```
app/
├── main.py              # FastAPI 入口
├── api/
│   ├── routes.py        # API 路由 (tts, upload, audio, voices)
│   └── schemas.py        # Pydantic 数据模型
├── services/
│   ├── tts_service.py   # TTS 引擎调度
│   ├── file_parser.py   # 文件解析 (TXT/PDF/DOCX/MD)
│   └── audio_storage.py # 音频存储
└── engines/
    ├── base.py          # 引擎抽象基类
    ├── edge_tts_engine.py   # Edge TTS (默认)
    ├── google_tts.py         # Google TTS
    └── pyttsx3_engine.py     # pyttsx3 (离线)

static/                  # 前端资源
├── index.html
├── css/styles.css
└── js/
    ├── api-client.js
    ├── app.js
    ├── audio-player.js  # 音频播放 + 进度条拖动
    └── file-handler.js
```

## 技术栈

- **前端**: Vanilla JS/CSS (无框架)
- **后端**: FastAPI + Python 3.11+
- **TTS 引擎**: edge-tts, gtts, pyttsx3
- **文件解析**: PyPDF2, python-docx, mistune

## 引擎优先级

1. **Edge TTS** - 免费、高质量、微软服务器
2. **Google TTS** - 备选方案
3. **pyttsx3** - 完全离线（仅 Windows）

## 依赖

```
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
python-multipart>=0.0.6
PyPDF2>=3.0.0
python-docx>=1.1.0
gtts>=2.5.0
pyttsx3>=2.90
httpx>=0.25.0
edge-tts>=7.0.0
mistune>=3.0.0
```

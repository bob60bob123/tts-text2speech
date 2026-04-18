# Text-to-Speech (TTS) 文字読み上げ

FastAPI + Microsoft Edge TTS に基づいた文字読み上げアプリケーションです。テキスト入力、ファイルアップロード、複数の音声選択、MP3ダウンロードをサポートしています。

## クイックスタート

```bash
# プロジェクトのクローン
git clone https://github.com/bob60bob123/tts-text2speech.git
cd tts-text2speech

# 依存関係のインストール
pip install -r requirements.txt

# サーバーの起動
start.bat をダブルクリック、または:
uvicorn app.main:app --host 0.0.0.0 --port 8000

# ブラウザで開く
# http://127.0.0.1:8000
```

## 機能

- **テキスト入力**: テキストを直接貼り付けて変換
- **ファイルアップロード**: TXT、PDF、DOCX、MD 形式をサポート
- **複数の音声**: 11種類のニューラルネットワーク音声（中英語）
- **再生制御**: 再生/一時停止、進捗ドラッグ、速度制御 (0.5x - 2.0x)
- **MP3保存**: 変換後に音声ファイルを保存

## 音声リスト

| 音声 ID                | 説明              |
| -------------------- | --------------- |
| zh-CN-XiaoxiaoNeural | シアオシアオ (女性-若年) |
| zh-CN-XiaoyiNeural   | シアオイ (女性-子供)   |
| zh-CN-YunxiaNeural   | ユンシア (女性-若年)   |
| zh-CN-YunxiNeural    | ユンシー (男性-若年)   |
| zh-CN-YunyangNeural  | ユンヤン (男性-中年)   |
| zh-CN-YunjianNeural  | ユンジエン (男性-若年)  |
| en-US-AriaNeural     | Aria (女性-米語)    |
| en-US-GuyNeural      | Guy (男性-米語)     |
| en-US-JennyNeural    | Jenny (女性-米語)   |
| en-GB-SoniaNeural    | Sonia (女性-英語)   |
| en-GB-RyanNeural     | Ryan (男性-英語)    |

## プロジェクト構造

```
app/
├── main.py              # FastAPI エントリーポイント
├── api/
│   ├── routes.py        # API ルーティング
│   └── schemas.py       # Pydantic モデル
├── services/
│   ├── tts_service.py   # TTS エンジン調整
│   ├── file_parser.py   # ファイル解析
│   └── audio_storage.py # 音声ストレージ
└── engines/
    ├── base.py          # エンジン抽象基底クラス
    ├── edge_tts_engine.py   # Edge TTS (デフォルト)
    ├── google_tts.py         # Google TTS
    └── pyttsx3_engine.py     # pyttsx3 (オフライン)

static/                  # フロントエンドリソース
├── index.html
├── css/styles.css
└── js/
    ├── api-client.js
    ├── app.js
    ├── audio-player.js  # 音声再生 + 進捗ドラッグ
    └── file-handler.js
```

## 技術スタック

- **フロントエンド**: Vanilla JS/CSS (フレームワークなし)
- **バックエンド**: FastAPI + Python 3.11+
- **TTS エンジン**: edge-tts, gtts, pyttsx3
- **ファイル解析**: PyPDF2, python-docx, mistune

## エンジン優先度

1. **Edge TTS** - 無料、高品質、Microsoft サーバー
2. **Google TTS** - バックアップオプション
3. **pyttsx3** - 完全オフライン（Windows のみ）

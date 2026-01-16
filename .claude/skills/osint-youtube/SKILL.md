---
name: osint-youtube
description: YouTube動画からOSINT情報を抽出するスキル。動画メタデータ取得、字幕ダウンロード、サムネイル取得、特定時間のフレーム抽出を行う。「この動画の情報を調べて」「字幕をダウンロードして」「サムネイルを取得して」などのリクエストで使用。
---

# OSINT YouTube Analysis

YouTube動画から情報を抽出するためのスキル。
**すべてのコマンドはDockerコンテナ経由で実行する。**

## 動画情報取得

### scripts/ytinfo.py

```bash
# 動画の基本情報（タイトル、投稿者、説明文、タグ等）
docker compose run --rm osint python /workspace/.claude/skills/osint-youtube/scripts/ytinfo.py \
  "https://youtu.be/cmpsALc_EGU"

# 利用可能な字幕一覧
docker compose run --rm osint python /workspace/.claude/skills/osint-youtube/scripts/ytinfo.py \
  "https://youtu.be/cmpsALc_EGU" --subtitles

# 字幕をダウンロード（複数言語対応）
docker compose run --rm osint python /workspace/.claude/skills/osint-youtube/scripts/ytinfo.py \
  "https://youtu.be/cmpsALc_EGU" --download-subs
```

## yt-dlp直接実行

### サムネイル取得

```bash
docker compose run --rm osint yt-dlp \
  --write-thumbnail --skip-download \
  -o "/workspace/challenges/<challenge>/evidence/%(title)s" \
  "https://youtu.be/xxx"
```

### 動画ダウンロード（フレーム抽出用）

```bash
# 動画全体
docker compose run --rm osint yt-dlp \
  -o "/workspace/challenges/<challenge>/evidence/%(title)s.%(ext)s" \
  "https://youtu.be/xxx"

# 特定の画質でダウンロード
docker compose run --rm osint yt-dlp \
  -f "best[height<=720]" \
  -o "/workspace/challenges/<challenge>/evidence/video.mp4" \
  "https://youtu.be/xxx"
```

### 字幕のみダウンロード

```bash
# 自動生成字幕を含む全字幕
docker compose run --rm osint yt-dlp \
  --write-auto-sub --write-sub \
  --sub-lang "en,ja,es,pt,zh,ko" \
  --sub-format "srt" \
  --skip-download \
  -o "/workspace/challenges/<challenge>/evidence/%(title)s" \
  "https://youtu.be/xxx"
```

## フレーム単位分析

YouTubeプレイヤーで `<` と `>` キーを使うとフレーム単位で移動可能。

### 特定時間のフレーム抽出

```bash
# 1. 動画をダウンロード
docker compose run --rm osint yt-dlp \
  -o "/workspace/challenges/<challenge>/evidence/video.mp4" \
  "https://youtu.be/xxx"

# 2. 特定時間のフレームを抽出（3分38秒）
docker compose run --rm osint ffmpeg \
  -i /workspace/challenges/<challenge>/evidence/video.mp4 \
  -ss 00:03:38 -frames:v 1 \
  /workspace/challenges/<challenge>/frames/frame_03_38.png
```

## チャンネル情報

```bash
# チャンネルの全動画一覧（メタデータのみ）
docker compose run --rm osint yt-dlp \
  --flat-playlist -j \
  "https://www.youtube.com/@gralhix/videos" | head -50
```

## 出力形式

```
## YouTube動画分析: <URL>

### 基本情報
- タイトル: ...
- チャンネル: ...
- アップロード日: YYYY-MM-DD
- 長さ: MM:SS

### 字幕
- 手動字幕: en, ja
- 自動字幕: en, es, ...

### 抽出フレーム
- frame_03_38.png (00:03:38)
```

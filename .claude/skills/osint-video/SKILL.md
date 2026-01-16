---
name: osint-video
description: 動画からOSINT情報を抽出するスキル。フレーム抽出、メタデータ解析、動画内テキストのOCRを行う。「この動画からフレームを抽出して」「動画のメタデータを確認して」「動画内のテキストを読み取って」などのリクエストで使用。
---

# OSINT Video Analysis

動画からインテリジェンス情報を抽出するためのスキル。

## ワークフロー

### 1. メタデータ確認（ffprobe）

```bash
# 基本情報
ffprobe -v quiet -print_format json -show_format <video>

# 詳細なストリーム情報
ffprobe -v quiet -print_format json -show_format -show_streams <video>
```

**重要なメタデータ:**
- `creation_time`: 作成日時
- `location`: 撮影位置（GPS）
- `encoder`: エンコーダー情報
- `duration`: 動画の長さ

### 2. フレーム抽出（ffmpeg）

```bash
# 5秒ごとにフレーム抽出
ffmpeg -i <video> -vf "fps=1/5" ./frames/frame_%04d.png

# 1秒ごとにフレーム抽出（詳細分析用）
ffmpeg -i <video> -vf "fps=1" ./frames/frame_%04d.png

# 特定時間のフレームを抽出（00:01:30の位置）
ffmpeg -i <video> -ss 00:01:30 -frames:v 1 frame.png

# キーフレームのみ抽出（高速）
ffmpeg -i <video> -vf "select='eq(pict_type,I)'" -vsync vfr ./frames/keyframe_%04d.png

# サムネイル生成（代表的なフレーム）
ffmpeg -i <video> -vf "thumbnail" -frames:v 1 thumbnail.png
```

### 3. 動画分析チェックリスト

| カテゴリ | 確認項目 |
|---------|---------|
| 音声 | 言語、BGM、環境音（交通音、鳥の声等） |
| テキスト | 字幕、ウォーターマーク、画面内テキスト |
| 動き | カメラの動き、被写体の移動方向 |
| 時間 | 光の変化、影の動き、時計 |
| 場所 | ランドマーク、建物、道路標識 |

### 4. 音声抽出

```bash
# 音声のみ抽出（MP3）
ffmpeg -i <video> -vn -acodec mp3 audio.mp3

# 音声のみ抽出（WAV、高品質）
ffmpeg -i <video> -vn -acodec pcm_s16le audio.wav
```

### 5. 特定シーンの切り出し

```bash
# 開始1分から30秒間を切り出し
ffmpeg -i <video> -ss 00:01:00 -t 00:00:30 -c copy clip.mp4

# 画質を下げてファイルサイズ削減
ffmpeg -i <video> -vf "scale=640:-1" -crf 28 small.mp4
```

## スクリプト

### scripts/extract_frames.py

動画からフレームを抽出し、各フレームのOCRも実行する。

```bash
python scripts/extract_frames.py <video_path> --interval 5 --ocr
```

**オプション:**
- `--interval`: フレーム抽出間隔（秒）
- `--output`: 出力ディレクトリ
- `--ocr`: 各フレームでOCRを実行
- `--lang`: OCR言語（デフォルト: eng）

## 出力形式

```
## 動画分析結果: <filename>

### メタデータ
- 長さ: 00:02:34
- 解像度: 1920x1080
- 作成日時: 2024-01-15 14:30:22
- フォーマット: MP4 (H.264)

### 抽出フレーム
- frames/frame_0001.png (00:00:00)
- frames/frame_0002.png (00:00:05)
- ...

### 検出テキスト
- Frame 3: "使用飞跃功能时..."
- Frame 7: "TOKYO-CITY"
```

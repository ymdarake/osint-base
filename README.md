# OSINT Base - SWIMMER OSINT CTF 2026 攻略基地

Claude Codeを活用したOSINT CTF攻略のための作業環境です。

## 大会情報

- **大会名**: SWIMMER OSINT CTF 2026
- **開催日時**: 2026年1月17日 12:10 (JST) - 18日 00:10 (JST)（12時間）
- **形式**: Jeopardy形式
- **チーム**: 最大6名

## ディレクトリ構造

```
osint-base/
├── CLAUDE.md           # OSINT分析官プロファイル（Claude Code用）
├── README.md           # このファイル
├── challenges/         # 課題ごとのワークスペース
│   └── challenge_XX/
│       ├── evidence/   # 収集した証拠
│       ├── frames/     # 動画フレーム
│       ├── notes.md    # 調査メモ
│       └── scripts/    # 一時スクリプト
├── tools/              # カスタムスクリプト
├── references/         # 参考資料
└── writeups/           # 解法メモ（大会後）
```

## セットアップ

### Option 1: Docker（推奨）

全ツールが入ったDockerイメージを使用：

```bash
# イメージをビルド
docker compose build

# コンテナに入って作業
docker compose run --rm osint bash

# ツール確認
osint-check

# Jupyter Notebookを起動（データ分析用）
docker compose --profile jupyter up jupyter
# http://localhost:8888 でアクセス
```

**同梱ツール:**
- exiftool（画像メタデータ）
- ffmpeg（動画処理）
- ripgrep（テキスト検索）
- tesseract-ocr（多言語OCR: 日/英/中/露/韓/アラビア）
- Python 3.11 + pandas, opencv, geopy 等

### Option 2: ローカルインストール

```bash
# macOS (Homebrew)
brew install exiftool ffmpeg ripgrep

# Python環境
pip install -r requirements.txt
```

## 新しい課題を開始する

```bash
# 課題ディレクトリを作成
mkdir -p challenges/challenge_XX/{evidence,frames,scripts}
touch challenges/challenge_XX/notes.md

# Claude Codeで作業開始
cd challenges/challenge_XX
```

## クイックコマンド

```bash
# 画像のGPS座標を確認
exiftool -GPS* <image>

# 動画から5秒ごとにフレーム抽出
ffmpeg -i <video> -vf "fps=1/5" ./frames/frame_%04d.png

# ディレクトリ内を再帰検索
rg "pattern" .
```

## 運用ルール

1. **15分ルール**: 1つの手掛かりに15分以上成果がなければ視点を変える
2. **証拠の保存**: 発見した証拠は必ず `evidence/` に保存
3. **パッシブ偵察のみ**: アクティブスキャン禁止

## 参考リンク

- [DIVER OSINT CTF](https://diverctf.org/)
- [CTFtime - SWIMMER](https://ctftime.org/event/2986/)
- [Overpass Turbo](https://overpass-turbo.eu/)
- [Wayback Machine](https://web.archive.org/)

---

*Good luck!*

# SWIMMER OSINT CTF 2026 Mission Profile

## Role

OSINT分析官として、公開情報のみを用いて課題を解決する。
思考プロセスは **OODAループ** で出力：

| Phase | 内容 |
|-------|------|
| Observe | 画像・動画・テキストから事実を抽出 |
| Orient | 手掛かりの分析と仮説構築 |
| Decide | 次に取るべきアクションを選択 |
| Act | ツールを使用して検証 |

---

## Constraints（絶対厳守）

| 禁止 | 許可 |
|------|------|
| アクティブスキャン（nmap, sqlmap等） | パッシブ偵察（検索、アーカイブ、Whois） |
| ソーシャルエンジニアリング | 公開DB参照（Shodan, MarineTraffic等） |
| 根拠なき推測（ハルシネーション） | 逆画像検索、衛星画像分析 |

---

## Tools

**すべてDockerコンテナ経由で実行:**

```bash
docker compose run --rm osint <command>
```

**スキル一覧** （詳細: `.claude/skills/<name>/SKILL.md`）

| スキル | 用途 | 主なコマンド/スクリプト |
|--------|------|------------------------|
| `osint-image` | 画像メタデータ、OCR | `exiftool`, `tesseract`, `analyze_image.py` |
| `osint-video` | 動画フレーム抽出 | `ffmpeg`, `ffprobe`, `extract_frames.py` |
| `osint-geoint` | 座標変換、地図リンク | `coord_links.py`, geopy |
| `osint-chrono` | カレンダー・時間変換 | `calendar_convert.py` |
| `osint-web` | Wayback Machine | `wayback.py` |
| `osint-youtube` | YouTube情報・字幕 | `ytinfo.py`, yt-dlp |

**クイック例:**

```bash
# 画像メタデータ
docker compose run --rm osint exiftool /workspace/challenges/<name>/evidence/image.jpg

# 座標→マップリンク生成
docker compose run --rm osint python /workspace/.claude/skills/osint-geoint/scripts/coord_links.py 35.6812 139.7671

# YouTube動画情報
docker compose run --rm osint python /workspace/.claude/skills/osint-youtube/scripts/ytinfo.py "https://youtu.be/xxx"

# Wayback Machineアーカイブ一覧
docker compose run --rm osint python /workspace/.claude/skills/osint-web/scripts/wayback.py "https://example.com" --list

# カレンダー変換（ペルシャ暦→グレゴリオ暦）
docker compose run --rm osint python /workspace/.claude/skills/osint-chrono/scripts/calendar_convert.py --from persian --to gregorian 1401 12 2
```

---

## 15分ルール

1つの手掛かりに15分以上成果がない → 視点を変える

---

## Directory Structure

```
challenges/<source>/<name>/
├── evidence/    # 収集した証拠
├── frames/      # 動画フレーム
└── writeup.md   # 解法メモ
```

---

## Flag Format

`Diver26{...}` または `Swimmer{...}`

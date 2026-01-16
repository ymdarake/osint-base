---
name: osint-web
description: Webアーカイブ調査スキル。Wayback Machineでのアーカイブ検索、削除されたコンテンツの復元、SNSアーカイブ調査を行う。「このURLの過去のバージョンを見たい」「削除されたページを探して」「ツイートのアーカイブを確認」などのリクエストで使用。
---

# OSINT Web Archive Investigation

Webアーカイブ調査のためのスキル。
**すべてのコマンドはDockerコンテナ経由で実行する。**

## Wayback Machine

Internet Archiveのアーカイブを検索・取得。

### scripts/wayback.py

```bash
# 最新のアーカイブを取得
docker compose run --rm osint python /workspace/.claude/skills/osint-web/scripts/wayback.py \
  "https://example.com"

# アーカイブ一覧（最新20件）
docker compose run --rm osint python /workspace/.claude/skills/osint-web/scripts/wayback.py \
  "https://example.com" --list

# 特定日付のアーカイブ
docker compose run --rm osint python /workspace/.claude/skills/osint-web/scripts/wayback.py \
  "https://example.com" --date 20230615
```

### 手動URL生成

```
https://web.archive.org/web/<YYYYMMDDHHMMSS>/<URL>
```

例: `https://web.archive.org/web/20230101120000/https://example.com`

## SNSアーカイブ

### Twitter/X

削除されたツイートの検索:
```bash
# Wayback Machineで検索
docker compose run --rm osint python /workspace/.claude/skills/osint-web/scripts/wayback.py \
  "https://twitter.com/username/status/1234567890" --list
```

Google検索: `site:web.archive.org twitter.com/username`

### Reddit

- **Unddit**: `https://www.unddit.com/r/<subreddit>/comments/<id>`
- **Reveddit**: `https://www.reveddit.com/`

### Facebook/Instagram

- Archive.todayでスナップショット確認
- `https://archive.today/<URL>`

## 有用なリソース

| サービス | 用途 | URL |
|---------|------|-----|
| Wayback Machine | Webアーカイブ | https://web.archive.org/ |
| Archive.today | スナップショット | https://archive.today/ |
| CachedView | Googleキャッシュ | https://cachedview.com/ |
| CachedPages | 複数キャッシュ検索 | https://www.cachedpages.com/ |

## 出力形式

```
## Webアーカイブ調査: <URL>

### アーカイブ履歴
- 最新: 2023-06-15 [リンク]
- 変更検出: 2023-03-01 [リンク]

### 発見した情報
- 削除前のコンテンツ: ...
- 変更点: ...
```

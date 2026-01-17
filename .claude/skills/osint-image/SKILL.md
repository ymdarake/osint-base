---
name: osint-image
description: 画像からOSINT情報を抽出するスキル。画像のメタデータ（EXIF、GPS座標、撮影日時）の解析、OCRによるテキスト抽出、画像内の特徴分析を行う。「この画像の撮影場所は？」「画像からテキストを読み取って」「EXIFデータを確認して」などのリクエストで使用。
---

# OSINT Image Analysis

画像からインテリジェンス情報を抽出するためのスキル。
**すべてのコマンドはDockerコンテナ経由で実行する。**

## ワークフロー

### 1. メタデータ抽出（exiftool）

```bash
# 全メタデータを表示
docker compose run --rm osint exiftool /workspace/challenges/<challenge>/evidence/<image>

# GPS座標のみ
docker compose run --rm osint exiftool -GPS* /workspace/challenges/<challenge>/evidence/<image>

# 撮影日時のみ
docker compose run --rm osint exiftool -CreateDate -DateTimeOriginal /workspace/challenges/<challenge>/evidence/<image>

# カメラ情報
docker compose run --rm osint exiftool -Make -Model -Software /workspace/challenges/<challenge>/evidence/<image>
```

**重要なEXIFフィールド:**
- `GPSLatitude`, `GPSLongitude`: 撮影位置
- `CreateDate`, `DateTimeOriginal`: 撮影日時
- `Make`, `Model`: カメラ機種
- `Software`: 編集ソフト（加工の痕跡）

### 2. OCR（tesseract）

```bash
# 基本OCR（英語）
docker compose run --rm osint tesseract /workspace/challenges/<challenge>/evidence/<image> stdout

# 日本語OCR
docker compose run --rm osint tesseract /workspace/challenges/<challenge>/evidence/<image> stdout -l jpn

# 多言語OCR
docker compose run --rm osint tesseract /workspace/challenges/<challenge>/evidence/<image> stdout -l jpn+eng+chi_sim+rus+kor+ara
```

**対応言語:** `ara`(アラビア), `chi_sim`(中国語), `eng`(英語), `jpn`(日本語), `kor`(韓国語), `rus`(ロシア語)

### 3. 画像分析チェックリスト

画像を分析する際に確認すべき項目：

| カテゴリ | 確認項目 |
|---------|---------|
| テキスト | 看板、標識、ナンバープレート、店名 |
| 建築様式 | 欧州風、アジア風、年代、素材 |
| 植生 | 樹木の種類、季節、気候帯 |
| 交通 | 右側/左側通行、車種、信号機 |
| 言語 | 文字体系（ラテン、キリル、漢字等） |
| 影 | 太陽の位置から時間帯・緯度を推定 |
| 天候 | 雲、湿度、季節の手掛かり |

### 4. 逆画像検索

画像の出典や類似画像を検索：
- Google Images: `https://images.google.com`
- Yandex Images: `https://yandex.com/images/` （ロシア・東欧に強い）
- TinEye: `https://tineye.com`
- PimEyes: `https://pimeyes.com` （顔認識専用）

## スクリプト

### scripts/reverse_search.py

逆画像検索サービスのURLを一括生成するスクリプト。

```bash
# 基本的な使用方法（検索URL一覧を生成）
docker compose run --rm osint python /workspace/.claude/skills/osint-image/scripts/reverse_search.py \
  /workspace/challenges/<challenge>/evidence/<image>

# 画像URLがある場合（直接検索URLを生成）
docker compose run --rm osint python /workspace/.claude/skills/osint-image/scripts/reverse_search.py \
  /workspace/challenges/<challenge>/evidence/<image> --url https://example.com/image.jpg

# ハッシュ値のみ表示
docker compose run --rm osint python /workspace/.claude/skills/osint-image/scripts/reverse_search.py \
  /workspace/challenges/<challenge>/evidence/<image> --hash-only
```

**出力内容:**
- 画像情報（ファイル名、サイズ、解像度）
- ハッシュ値（MD5、SHA256）
- 各検索サービスへのリンク
  - Google Lens, Google Images, Yandex, TinEye, Bing
  - 顔認識: PimEyes, FaceCheck, Search4Faces
  - Reddit専用: KarmaDecay

### scripts/analyze_image.py

画像のメタデータとOCRを一括実行するスクリプト。

```bash
docker compose run --rm osint python /workspace/.claude/skills/osint-image/scripts/analyze_image.py \
  /workspace/challenges/<challenge>/evidence/<image> --lang jpn+eng
```

## 出力形式

```
## 画像分析結果: <filename>

### メタデータ
- GPS: 35.6762° N, 139.6503° E
- 撮影日時: 2024-01-15 14:30:22
- カメラ: iPhone 14 Pro

### OCRテキスト
[抽出されたテキスト]

### 視覚的特徴
- 言語: 日本語、英語
- 建築様式: 現代的な商業ビル
- 交通: 左側通行
```

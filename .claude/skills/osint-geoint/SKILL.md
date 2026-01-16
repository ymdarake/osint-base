---
name: osint-geoint
description: 地理空間情報（GEOINT）を扱うスキル。座標変換、Overpass Turboクエリ生成、what3words変換、ジオロケーション支援を行う。「この座標をGoogle Mapsで表示」「Overpass Turboでクエリを作成して」「what3wordsを座標に変換」「この場所の周辺施設を調べて」などのリクエストで使用。
---

# OSINT GEOINT (Geospatial Intelligence)

地理空間情報を扱うためのスキル。
**Pythonコードの実行はDockerコンテナ経由で行う。**

## 座標形式の変換

### 主要な座標形式

| 形式 | 例 | 用途 |
|------|-----|------|
| 度分秒 (DMS) | 35°41'22"N, 139°45'30"E | 地図、GPS |
| 10進数 (DD) | 35.6894, 139.7583 | Google Maps、API |
| UTM | 54S 389456 3948234 | 軍事、測量 |

### 変換ツール（Docker経由）

```bash
# DMS → DD
docker compose run --rm osint python -c "
from geopy.point import Point
point = Point(\"35°41'22\\\"N 139°45'30\\\"E\")
print(f'{point.latitude}, {point.longitude}')
"

# 住所 → 座標
docker compose run --rm osint python -c "
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent='osint')
location = geolocator.geocode('東京駅')
print(f'{location.latitude}, {location.longitude}')
"

# 座標 → 住所（逆ジオコーディング）
docker compose run --rm osint python -c "
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent='osint')
location = geolocator.reverse('35.6812, 139.7671')
print(location.address)
"
```

## Overpass Turbo クエリ

OpenStreetMapのデータをクエリするためのツール。
URL: https://overpass-turbo.eu/

### 基本クエリ構文

```
[out:json][timeout:25];
// 検索対象
(
  node["key"="value"](bbox);
  way["key"="value"](bbox);
  relation["key"="value"](bbox);
);
out body;
>;
out skel qt;
```

### よく使うクエリ例

**特定エリア内の滑走路:**
```
[out:json];
area["name"="大同市"]->.searchArea;
(
  way["aeroway"="runway"](area.searchArea);
);
out body;
>;
out skel qt;
```

**座標周辺のレストラン（半径500m）:**
```
[out:json];
(
  node["amenity"="restaurant"](around:500, 35.6812, 139.7671);
);
out body;
```

**特定の店名を検索:**
```
[out:json];
(
  node["name"~"TOKYO-CITY", i];
  way["name"~"TOKYO-CITY", i];
);
out body;
>;
out skel qt;
```

### OSMタグ早見表

| カテゴリ | タグ |
|---------|-----|
| 空港 | `aeroway=aerodrome` |
| 滑走路 | `aeroway=runway` |
| 鉄道駅 | `railway=station` |
| バス停 | `highway=bus_stop` |
| レストラン | `amenity=restaurant` |
| ホテル | `tourism=hotel` |
| 学校 | `amenity=school` |
| 病院 | `amenity=hospital` |

## what3words

3単語で位置を表すシステム。
URL: https://what3words.com/

**変換方法:**
1. what3wordsサイトで3単語を入力
2. 表示された座標をコピー

**例:**
- `///ブムバ.ツォグツ.バタトガフ` → モンゴル・ウランバートル

## ジオロケーション手順

### 1. 初期分析

画像から以下を特定：
- 言語/文字（看板、標識）
- 建築様式（欧州、アジア、中東）
- 交通ルール（右側/左側通行）
- 植生、地形、気候

### 2. エリア絞り込み

- Google検索: キーワード + "location"
- 逆画像検索: Google, Yandex
- ランドマーク検索

### 3. 精密位置特定

1. Google Earth / Google Maps
2. ストリートビューで照合
3. 衛星画像で確認

### 4. 時間特定（Chronolocation）

- Google Earth Pro: Historical Imagery
- 建物の建設状況
- 影の長さ/方向 → 太陽位置計算

## スクリプト

### scripts/coord_links.py

座標から各種マップサービスのリンクを一括生成。

```bash
docker compose run --rm osint python /workspace/.claude/skills/osint-geoint/scripts/coord_links.py 41.352757 -4.690017
```

**出力例:**
- Google Maps, Earth, StreetView
- OpenStreetMap, Yandex, Bing
- what3words, SunCalc, Sentinel Hub
- Overpass Turbo

## 出力形式

```
## ジオロケーション結果

### 特定場所
- 名称: [場所名]
- 座標: 35.6812, 139.7671
- Google Maps: https://maps.google.com/?q=35.6812,139.7671

### 根拠
1. [画像の特徴1]: [根拠説明]
2. [画像の特徴2]: [根拠説明]

### 確信度
高 / 中 / 低
```

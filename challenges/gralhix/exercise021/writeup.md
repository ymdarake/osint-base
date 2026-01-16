# OSINT Exercise #021 解答

**問題:** Gralhix OSINT Exercise #021
**難易度:** Easy
**カテゴリ:** GEOINT（地理空間情報）
**出典:** https://gralhix.com/list-of-osint-exercises/osint-exercise-021/

## 課題

チョコレートバーに刻印された地図と、同じ場所の衛星画像から座標を特定する。

---

## 分析プロセス

### Observe（観察）

画像の特徴：
- **左側（チョコレート）**: 道路網、蛇行する川、円形の構造物が刻印
- **右側（衛星画像）**: 蛇行する川、農地、森林、白い砂浜/ビーチ

### Orient（状況判断）

1. チョコレートのブランドロゴを逆画像検索 → **Puchero** と特定
2. Pucheroはスペインのコーヒー・チョコレートブランド
3. 会社所在地: Carretera N-601 Km-155, 47238 Hornillos de Eresma, **Valladolid, Spain**

### Decide（意思決定）

スペイン・バリャドリッド近郊の **Tierra de Pinares** 地域を調査

### Act（実行）

Google Mapsで川の蛇行パターンを照合 → 一致確認

---

## 解答

### 特定場所
- **地域**: Tierra de Pinares, Castilla y León, Spain
- **座標**: `41.352757, -4.690017`
- **Google Maps**: https://maps.google.com/?q=41.352757,-4.690017

### 確信度: 高

川の蛇行パターン、道路配置、地形が完全に一致。

---

## 学んだこと

1. **ブランドロゴは重要な手がかり** - 製品のロゴから会社所在地を特定可能
2. **地形パターンマッチング** - 川の蛇行は指紋のようにユニーク
3. **注意**: この画像では北が下向き（通常と逆の向き）

---

## 使用ツール

- 逆画像検索（Google Lens）
- Google Maps / Google Earth

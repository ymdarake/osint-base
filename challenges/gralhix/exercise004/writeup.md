# Exercise 004: Island Resort Identification

## 問題
島のリゾートの空撮写真から以下を特定する:
- a) リゾートの名前
- b) 島の座標
- c) 写真撮影時のカメラの向き（方位）

## 解答

| 質問 | 回答 |
|------|------|
| a) リゾートの名前 | **Oan Resort** |
| b) 島の座標 | **7.3626, 151.7563** (7°21'45.36"N 151°45'22.68"E) |
| c) カメラの向き | **北西方向 (North-West)** |

## OODAループ分析

### Observe（観察）

**画像から抽出した事実:**
- 熱帯の小島（楕円形、ヤシの木が密生）
- 白い砂浜とターコイズブルーの浅瀬
- サンゴ礁に囲まれている
- 背景に他の島（左に山のある大きな島、奥に小さな島）
- ドローンによる空撮写真
- 砂浜に小型ボートが停泊

**メタデータ:**
- 写真家: Jonathan Jensen
- GPS座標: メタデータには含まれていない
- ソフトウェア: Google

### Orient（状況判断）

**手がかりの分析:**
1. 島の形状と周囲の環境から、太平洋の環礁内に位置すると推測
2. 背景の山のある島は、環礁内の主要な火山島と思われる
3. Jonathan Jensenで直接検索しても場所は特定できず
4. 逆画像検索（Gemini）でOan Resort, Chuuk（チューク）と特定

**仮説:**
- チューク環礁（旧トラック諸島）内の小島
- 背景の島はWeno島またはTonoas島

### Decide（決定）

1. 逆画像検索でリゾート名を特定
2. 座標をWeb検索で確認
3. Google Earth Proで背景の島を照合し、カメラの向きを検証

### Act（検証）

**使用ツール:**
- `exiftool`: メタデータ抽出（GPS情報なし）
- Gemini analyzeFile: 逆画像検索でOan Resortを特定
- WebSearch: 座標の確認
- WebFetch: 詳細情報の取得

**検証結果:**
- 座標 7.3626, 151.7563 でGoogle Mapsを確認 → Oan Islandと一致
- 背景の島々の配置がGoogle Earth Proの北西方向ビューと一致

## 地図リンク

| サービス | リンク |
|----------|--------|
| Google Maps | https://maps.google.com/?q=7.3626,151.7563 |
| Google Earth | https://earth.google.com/web/@7.3626,151.7563,500a,35y,0h,0t,0r |
| OpenStreetMap | https://www.openstreetmap.org/?mlat=7.3626&mlon=151.7563&zoom=15 |

## 所在地情報

- **国**: ミクロネシア連邦
- **州**: チューク州（旧トラック州）
- **環礁**: チューク環礁（Chuuk Lagoon / 旧Truk Lagoon）
- **自治体**: Parem Municipality, Wonip

## 背景の島の特定

カメラが北西を向いていることから:
- **左奥の山のある大きな島**: Tonoas (Dublon) 島またはWeno (Moen) 島
- **中央奥の平坦な島**: Eten島などの環礁内の小島

## 参考資料

- [Oan Resort - Sandee](https://sandee.com/micronesia/chuuk/wonip/oan-resort)
- [Sofia's OSINT Exercise 004 Walkthrough](https://mugr.at/walkthroughs/sofias-osint-004/)
- [Chuuk Lagoon - Wikipedia](https://en.wikipedia.org/wiki/Chuuk_Lagoon)

## 学んだこと

1. **逆画像検索の活用**: メタデータにGPS情報がなくても、画像の特徴から場所を特定できる
2. **Google Earth Proの活用**: 3Dビューで背景の島を照合することで、カメラの向きを特定できる
3. **環礁の地理**: チューク環礁は第二次世界大戦の沈船ダイビングで有名な場所

---
*Exercise 004 完了*

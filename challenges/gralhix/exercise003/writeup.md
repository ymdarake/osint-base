# OSINT Exercise #003 解答

**問題:** Gralhix OSINT Exercise #003
**難易度:** Medium
**カテゴリ:** GEOINT（建物特定）
**出典:** https://gralhix.com/list-of-osint-exercises/osint-exercise-003/

## 課題

2017年4月、ソマリア大統領ファルマージョがトルコを訪問し、エルドアン大統領と握手している写真が公開された。撮影場所の名前と座標を特定せよ。

---

## 分析プロセス

### Observe（観察）

画像から見える特徴：
- **紋章:** トルコ大統領紋章（16角星、金色）が入口上部に
- **建築:** 金色の装飾的な大きな入口、白い柱
- **国旗:** 左にソマリア国旗、右にトルコ国旗
- **カーペット:** 青いカーペット（儀礼用）
- **文脈:** 公式な首脳会談の場

### Orient（状況判断）

**仮説:** トルコが外国首脳を迎える公式施設

調査結果：
1. トルコ大統領府複合施設（Cumhurbaşkanlığı Külliyesi）が外国首脳の公式歓迎場所
2. 2014年10月29日に開設
3. 通称「Ak Saray」（白い宮殿）
4. アンカラのBeştepe地区、Atatürk Forest Farm内に位置

### Decide（意思決定）

大統領府複合施設の座標を地図・地理情報源から取得

### Act（実行）

複数のソースから座標を確認：
- Wikidata
- Mapcarta
- AroundUs

---

## 解答

### 場所
**Presidential Complex of Turkey（トルコ大統領府複合施設）**
- トルコ語: Cumhurbaşkanlığı Külliyesi
- 別名: Ak Saray, Beştepe Presidential Complex

### 座標
- **DD形式:** 39.9308, 32.7989
- **DMS形式:** 39°55'50.88"N 32°47'56.04"E

### 検証リンク
- [Google Maps](https://maps.google.com/?q=39.9308,32.7989)
- [Google Earth](https://earth.google.com/web/@39.9308,32.7989,500a,35y,0h,0t,0r)

### 確信度: 高

---

## 使用した手がかり

| 手がかり | 推論 |
|---------|------|
| トルコ大統領紋章 | トルコ政府の公式施設 |
| 両国旗の配置 | 国際的な公式会談 |
| 建築様式 | 大規模な儀礼用施設 |
| 青いカーペット | 外国首脳歓迎の儀礼 |

---

## 学んだこと

1. **紋章・シンボルは強力な手がかり** - 国家紋章から公式施設を特定
2. **儀礼的要素に注目** - カーペット、国旗配置が公式行事を示唆
3. **「どこで外国首脳を迎えるか」という視点** - 建物の用途から検索
4. **複数のソースで座標を確認** - Wikidata、地図サービス等

---

## 参考

- [Presidential Complex (Turkey) - Wikipedia](https://en.wikipedia.org/wiki/Presidential_Complex_(Turkey))
- [Wikidata - Presidential Complex of Turkey](https://www.wikidata.org/wiki/Q40894456)

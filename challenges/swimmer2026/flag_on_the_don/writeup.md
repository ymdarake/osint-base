# SWIMMER CTF 2026 - flag_on_the_don（太鼓の達人会場特定）

## 問題

> 2025年8月28日、群馬県で「太鼓の達人」を利用したイベントが開催されました。
> その会場となった建物はどこでしょうか。
> OpenStreetMapのウェイ（way）番号で解答してください。

## Flag

```
SWIMMER{1055932712}
```

> **注記**: 本問題はチームメンバーが解答。以下は調査過程の記録。

## 解法

### Observe（観察）

- 問題: 2025年8月28日に群馬県で開催された太鼓の達人イベントの会場を特定
- 回答形式: OpenStreetMapのway番号

### Orient（分析）

**ヒント情報**: JOMOスクエアでのイベント

**JOMOスクエアの調査:**
- 所在地: 群馬県前橋市古市町一丁目50-22
- 座標: 36.377203, 139.048196（[office-navi](https://en.office-navi.jp/building/15000101/)より）
- 建物: 地上9階建て、2025年7月竣工
- 用途: 商業複合施設（上毛新聞社が開発）
- 1階に「学びの場」というイベントスペースあり

**OSM調査:**
JOMOスクエアは2025年7月竣工の新しい建物のため、OSMに「JOMOスクエア」という名前では登録されていない。

座標周辺100m以内の建物を調査:

| way番号 | 距離 | タイプ | ノード数 |
|---------|------|--------|----------|
| 1277596118 | 87m | roof | 5 |
| 1055932712 | 98m | commercial | 7 |
| 447983315 | 109m | yes | 5 |
| 1277855834 | 143m | yes (6階) | 37 |

### Decide（決定）

- way/1277596118: `building=roof`（屋根構造物）→ 対象外
- way/1055932712: `building=commercial`（商業建物）→ **最有力候補**
- way/1277855834: ホテルラシーネ → 別の建物

JOMOスクエアは商業ビルであり、`building=commercial`タグが付いた**way/1055932712**が最も適合する。

### Act（実行）

OpenStreetMapで確認:
- URL: https://www.openstreetmap.org/way/1055932712
- changeset: 150625343（2024年4月）

## 参考資料

- [JOMOスクエア - オフィスナビ](https://en.office-navi.jp/building/15000101/)
- [上毛新聞社 JOMOスクエア完成](https://www.jomo-news.co.jp/articles/-/713195)
- [群馬県eスポーツ連合](https://gunma-esu.com/)
- [OpenStreetMap way/1055932712](https://www.openstreetmap.org/way/1055932712)

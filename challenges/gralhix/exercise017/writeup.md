# OSINT Exercise #017 解答

**問題:** Gralhix OSINT Exercise #017
**難易度:** Medium
**カテゴリ:** カレンダー変換
**出典:** https://gralhix.com/list-of-osint-exercises/osint-exercise-017/

## 課題

3つの異なるカレンダーシステムを使用する国の記事について、グレゴリオ暦での公開日を特定せよ。

---

## 分析プロセス

### Observe（観察）

3つの記事リンクが提供された：

1. **エチオピア記事** - hatricksport.net（東京マラソン優勝者）
2. **ネパール記事** - onlinekhabar.com（警察採用）
3. **ペルシャ記事** - yjc.ir（Fajr音楽祭）

### Orient（状況判断）

各国が使用するカレンダーシステム：

| 国 | カレンダー | 特徴 |
|----|-----------|------|
| エチオピア | エチオピア暦 | グレゴリオ暦より約7-8年遅れ |
| ネパール | ビクラム・サンバト暦 | グレゴリオ暦より約56-57年先 |
| イラン | 太陽暦ヒジュラ暦 | 春分の日を年始とする |

### Decide（意思決定）

各記事にアクセスし、日付を抽出してグレゴリオ暦に変換する。

### Act（実行）

#### 1. エチオピア記事

**URL:** https://www.hatricksport.net/ኢትዮጵያዊው-አትሌት-የቶኪዮ-ማራቶን-ባለ/

**発見した日付:**
- HTMLメタデータ `datetime="2020-03-01T08:37:13+03:00"`
- ページ表示: "6 years ago"

**内容:** 第14回東京マラソンでビルハヌ・レゲセが優勝（2:04:15）

**グレゴリオ暦:** 2020年3月1日

#### 2. ネパール記事

**URL:** https://www.onlinekhabar.com/2016/01/381827

**発見した日付:** २०७२ माघ १७ गते १८:२४
- 2072年 マーグ月 17日（ビクラム・サンバト暦）

**変換:**
- マーグ月は10番目の月（1月中旬〜2月中旬に相当）
- 2072 BS = 2015-2016 AD

**グレゴリオ暦:** 2016年1月31日

#### 3. ペルシャ記事

**URL:** https://www.yjc.ir/fa/news/8369785/... （Wayback Machine経由でアクセス）

**発見した日付:** ۰۲ اسفند ۱۴۰۱
- 1401年 エスファンド月 2日（太陽暦ヒジュラ暦）

**変換:**
- エスファンド月は12番目の月（2月下旬〜3月に相当）
- 1401 SH = 2022-2023 AD

**グレゴリオ暦:** 2023年2月21日

---

## 解答

| 記事 | 現地暦の日付 | グレゴリオ暦 |
|------|-------------|-------------|
| エチオピア | （メタデータに格納） | **2020年3月1日** |
| ネパール | 2072 माघ 17 | **2016年1月31日** |
| ペルシャ | 1401 اسفند 2 | **2023年2月21日** |

---

## 使用したツール・リソース

| ツール | 用途 |
|--------|------|
| Playwright MCP | 各サイトへのアクセス |
| Wayback Machine | ペルシャサイト（アクセス不可）のアーカイブ取得 |
| Web検索 | カレンダー変換確認 |

### カレンダー変換リソース

- [Nepali Date Converter - Hamro Patro](https://www.hamropatro.com/date-converter)
- [Iran Chamber Society Calendar Converter](https://www.iranchamber.com/calendar/converter/iranian_calendar_converter.php)
- [Ethiopian Calendar Converter](https://www.ethiopiancalendar.net/converter.html)

---

## 学んだこと

1. **HTMLメタデータの活用** - 表示上は現地暦でも、datetimeにはISO形式のグレゴリオ暦が格納されていることがある
2. **Wayback Machineの重要性** - アクセス不可のサイトもアーカイブから情報取得可能
3. **カレンダーシステムの理解** - 各国の暦システムを知ることでOSINT調査の幅が広がる
4. **月の対応関係** - 現地暦の月がグレゴリオ暦のどの時期に対応するか把握することが重要

---

## 参考

- [Solar Hijri calendar - Wikipedia](https://en.wikipedia.org/wiki/Solar_Hijri_calendar)
- [Vikram Samvat - Wikipedia](https://en.wikipedia.org/wiki/Vikram_Samvat)
- [Ethiopian calendar - Wikipedia](https://en.wikipedia.org/wiki/Ethiopian_calendar)

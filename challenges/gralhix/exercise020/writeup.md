# OSINT Exercise 020 - Wayback Machine Investigation

## 課題概要

この課題は「過去のコンテンツを見つける」系の問題で、Wayback Machineを使って削除されたWebページや過去の情報を発見する技術を習得することが目的。

**課題URL**: https://gralhix.com/list-of-osint-exercises/osint-exercise-020/
- 現在は「Oops! That page can't be found.」と表示される（これ自体がパズル）

## タスク

1. OSINT Exercise #020のページを見つける
2. 2000年のx.comウェブサイト内のFAQページを見つける
3. 2000年7月のx.comの経営陣リストを特定する

---

## OODAループ分析

### Observe（観察）

- 課題ページが404エラーを返す
- 隠しリンク（https://gralhix.com/wp-content/uploads/2023/08/so-close-i-can-almost-taste-it.png）はスポンジボブのミーム画像「SO CLOSE I CAN ALMOST TASTE IT」
- x.comは2000年当時、Elon Muskが創業したオンライン銀行（後にPayPalと合併）

### Orient（状況判断）

- Wayback Machineで過去のページを復元する必要がある
- x.comの2000年当時のURL構造を調査する必要がある
- CDX APIを使用して過去のURLを網羅的に検索可能

### Decide（意思決定）

1. exercise 020のWayback Machineアーカイブを検索
2. x.comの2000年のサイト構造をCDX APIで調査
3. FAQと経営陣ページの具体的なURLを特定

### Act（実行）

Wayback Machine検索スクリプトとCDX APIを活用して調査を実施。

---

## 解答

### Task 1: OSINT Exercise #020ページの発見

**使用ツール**: `wayback.py`

```bash
docker compose run --rm osint python /workspace/.claude/skills/osint-web/scripts/wayback.py \
  "https://gralhix.com/list-of-osint-exercises/osint-exercise-020/" --list
```

**結果**: 2023年8月28日以降の複数のアーカイブを発見

**アーカイブURL**:
```
https://web.archive.org/web/20230828083935/https://gralhix.com/list-of-osint-exercises/osint-exercise-020/
```

---

### Task 2: 2000年のx.com FAQページ

**調査手順**:

1. CDX APIでx.comの2000年のURL構造を調査
```bash
curl -s "https://web.archive.org/cdx/search/cdx?url=x.com/help*&from=1999&to=2001&output=text&fl=original,timestamp&limit=50"
```

2. FAQページのパターンを発見: `help_faq.asp`, `help_faq.htm`

**結果**:

| 日時 | URL |
|------|-----|
| 2000-03-02 | http://www.x.com/help_faq.asp |
| 2000-03-04 | http://x.com/help_faq.htm |
| 2000-06-18 | http://www.x.com/help_faq.htm |
| 2000-10-02 | http://www.x.com/help_faq.htm |

**FAQページURL**:
```
https://web.archive.org/web/20000618112127/http://www.x.com/help_faq.htm
```

**FAQの主な内容**:
- About X.com（会社概要）
- Banking Services（銀行サービス）
- X.com Funds（投資信託）
- ATM services（ATMサービス）
- Customer Service（カスタマーサービス）
- Security & Privacy（セキュリティとプライバシー）
- Account Maintenance（アカウント管理）

**注目ポイント**:
- X.comは1999年3月にElon Muskによって設立
- Sequoia CapitalのMichael Moritzから資金調達（Yahoo!, WebVan, eToys等にも投資）
- First Western National Bankとの提携でFDIC保険対象

---

### Task 3: 2000年7月のx.com経営陣リスト

**調査手順**:

1. CDX APIで経営陣ページを検索
```bash
curl -s "https://web.archive.org/cdx/search/cdx?url=x.com/about*&from=1999&to=2001&output=text&fl=original,timestamp&limit=50"
```

2. `about_management.htm` を発見

**経営陣ページURL**:
```
https://web.archive.org/web/20000706205553/http://www.x.com/about_management.htm
```
（アーカイブ日時: 2000年7月6日）

**経営陣リスト（2000年7月時点）**:

| 名前 | 役職 |
|------|------|
| **Elon Musk** | President and Chief Executive Officer, Founder of X.com |
| **Peter Thiel** | Chairman and Co-founder of PayPal.com |
| **John T. Story** | Executive Vice President |
| **Dave Johnson** | Chief Financial Officer |
| **Kathy Donovan** | Chief Credit Officer |
| **Sanjay Bhargava** | Vice President, ePayments |
| **Mark Sullivan** | Vice President, Operations |

**経営陣の経歴要約**:

1. **Elon Musk**: 1999年3月にX.comを創業。1995年にZip2 Corp.を設立し、1999年にCompaq/AltaVistaに$305Mで売却。Wharton School（ファイナンス）とUniversity of Pennsylvania（物理学）卒業。

2. **Peter Thiel**: Confinity/PayPalの共同創業者。Thiel Capital Management, LLCを運営。Credit Suisseでオプショントレーダー、Sullivan & Cromwellで証券弁護士の経験。Stanford University（BA, JD）卒業。

3. **John T. Story**: 約30年の投資信託・国際投資経験。元Montgomery Asset Management EVP、Alliance Capital Management SVP。

4. **Dave Johnson**: 元Banc of America Securities CFO/CAO。Bank of Americaで19年の経験。

5. **Kathy Donovan**: 25年以上の銀行経験。元Citibank California/Nevada Small Business Lending Credit Director。

6. **Sanjay Bhargava**: 10年以上のグローバル決済経験。元Citibank VP of Strategy & Quality。IIT Bombay（機械工学）、IIM Ahmedabad（MBA）卒業。

7. **Mark Sullivan**: 元First Data Investor Services Group VP、Montgomery Asset Management VP。

---

## 歴史的背景

- **1999年3月**: Elon MuskがX.comを設立
- **2000年3月**: X.comとConfinity（PayPal）が合併
- **2000年5月**: Bill Harris（元Intuit CEO）が退任、Elon MuskがCEOに復帰
- **2000年7月**: 本アーカイブの時点（Musk CEO、Thiel Chairman）
- **2000年9月**: 取締役会がMuskをCEOから解任、Peter ThielがCEOに就任
- **2001年6月**: 社名をPayPalに変更
- **2002年**: eBayがPayPalを$1.5Bで買収

---

## 使用ツールとテクニック

1. **Wayback Machine** (`wayback.py`)
   - 削除されたページのアーカイブ検索
   - 過去のWebサイト状態の復元

2. **CDX API**
   - URL構造の網羅的検索
   - 特定期間のアーカイブ一覧取得
   ```
   https://web.archive.org/cdx/search/cdx?url=x.com/*&from=2000&to=2000&output=text&fl=original,timestamp
   ```

3. **curl**
   - Wayback Machineアーカイブの直接取得

---

## 教訓

1. **URL構造の変遷を考慮する**: 2000年当時は `.asp`, `.htm` 拡張子が一般的
2. **CDX APIは強力なツール**: ワイルドカード検索で過去のサイト構造を把握可能
3. **複数のアーカイブ日付を確認**: 同じページでも時期によって内容が異なる
4. **httpとhttpsの違い**: 過去のアーカイブはhttp://が一般的

---

## 参考リンク

- [Wayback Machine](https://web.archive.org/)
- [CDX Server API](https://github.com/internetarchive/wayback/tree/master/wayback-cdx-server)
- [X.com (bank) - Wikipedia](https://en.wikipedia.org/wiki/X.com_(bank))

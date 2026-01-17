# Truck at 11foot8 Bridge - OSINT Challenge

## Challenge

あるトラックが Plus Code `8773X3XQ+JWQ` を2025年6月21日 13:39:54（現地時間）ごろに通過しました。このトラックの車体に書かれていたFQDNを解答してください。

## Answer

**SWIMMER{www.miraclemoversusa.com}**

---

## OODA Loop Analysis

### Observe（観察）

1. **Plus Code の解析**
   - Plus Code: `8773X3XQ+JWQ`
   - 変換結果: 35.999063, -78.910188
   - 場所: Durham, North Carolina, USA

2. **場所の特定**
   - 座標は有名な「11foot8 Bridge」（Can Opener Bridge）の場所
   - 住所: 201 South Gregson Street, Durham, NC
   - この橋は低い高さ（12'4"）で多くのトラックが衝突することで有名

3. **映像の発見**
   - 11foot8.com で2025年6月21日の衝突記録（crash #187）を発見
   - YouTube動画: https://www.youtube.com/watch?v=MJ4tpEhQ86g
   - 動画タイムスタンプ: 2025-06-21 13:39:53（問題の時刻と一致）

### Orient（状況判断）

- Plus Code の場所は11foot8 Bridge
- この場所では橋に衝突するトラックが定点カメラで撮影されている
- 2025年6月21日13:39頃の映像が公開されている
- トラックは引越し業者「Miracle Movers」の車両

### Decide（決心）

YouTube動画からトラックの車体に書かれている情報を読み取る。

### Act（実行）

1. YouTube動画を再生し、トラックが映っているフレームをキャプチャ
2. 画像分析でトラック車体のテキストを解読
3. FQDNを特定

---

## Evidence（証拠）

### 場所の特定

| 項目 | 値 |
|------|-----|
| Plus Code | 8773X3XQ+JWQ |
| 座標 | 35.999063, -78.910188 |
| 場所 | 11foot8 Bridge (Can Opener Bridge) |
| 住所 | 201 South Gregson Street, Durham, NC |

### トラックの情報

| 項目 | 値 |
|------|-----|
| 会社名 | Miracle Movers |
| FQDN | www.MiracleMoversUSA.com |
| 電話番号 | (919) 416-4043 |
| スローガン | "Your Property Is In Our Hands" |
| サービス | Professional, Reliable & Courteous Moving Service |
| 種類 | Local and Long Distance |

### 衝突記録

- 11foot8.com crash #187
- 日時: 2025年6月21日 13:39:53
- 動画: https://www.youtube.com/watch?v=MJ4tpEhQ86g
- チャンネル: yovo68 (@11foot8plus8)

---

## Screenshots

- `evidence/youtube_truck_frame2.png` - トラックの側面が映ったフレーム（FQDN確認用）
- `evidence/youtube_truck_fullscreen.png` - 全画面キャプチャ
- `evidence/youtube_truck_arriving.png` - トラック到着シーン

---

## References

- [11foot8.com](https://11foot8.com/) - The Can Opener Bridge
- [Miracle Movers USA](https://www.miraclemoversusa.com/) - 会社公式サイト
- [Plus Codes](https://plus.codes/) - Open Location Code

---
name: osint-chrono
description: 時間情報（Chronolocation）を扱うスキル。カレンダー変換（エチオピア、ネパール、ペルシャ、イスラム暦）、タイムゾーン変換、太陽位置計算を行う。「この日付をグレゴリオ暦に変換」「ペルシャ暦1401年の日付は？」「影の角度から時刻を特定」などのリクエストで使用。
---

# OSINT Chrono (Time Intelligence)

時間情報を扱うためのスキル。
**すべてのコマンドはDockerコンテナ経由で実行する。**

## カレンダー変換

### 対応カレンダー

| カレンダー | 地域 | 特徴 |
|-----------|------|------|
| Gregorian | 世界標準 | 西暦 |
| Persian (Jalali) | イラン、アフガニスタン | 太陽暦ヒジュラ暦、春分が年始 |
| Islamic (Hijri) | イスラム圏 | 太陰暦ヒジュラ暦、月の周期基準 |
| Nepali (Bikram Sambat) | ネパール | グレゴリオ暦より約57年先 |
| Ethiopian | エチオピア | グレゴリオ暦より約7-8年遅れ |

### scripts/calendar_convert.py

```bash
# ペルシャ暦 → グレゴリオ暦
docker compose run --rm osint python /workspace/.claude/skills/osint-chrono/scripts/calendar_convert.py \
  --from persian --to gregorian 1401 12 2

# ネパール暦 → グレゴリオ暦
docker compose run --rm osint python /workspace/.claude/skills/osint-chrono/scripts/calendar_convert.py \
  --from nepali --to gregorian 2072 10 17

# イスラム暦 → グレゴリオ暦
docker compose run --rm osint python /workspace/.claude/skills/osint-chrono/scripts/calendar_convert.py \
  --from islamic --to gregorian 1445 7 15

# グレゴリオ暦 → 全カレンダー表示
docker compose run --rm osint python /workspace/.claude/skills/osint-chrono/scripts/calendar_convert.py \
  --from gregorian --to all 2023 2 21
```

### 月名対応表

**ペルシャ暦 (Persian/Jalali):**
1. Farvardin (3-4月)
2. Ordibehesht (4-5月)
3. Khordad (5-6月)
4. Tir (6-7月)
5. Mordad (7-8月)
6. Shahrivar (8-9月)
7. Mehr (9-10月)
8. Aban (10-11月)
9. Azar (11-12月)
10. Dey (12-1月)
11. Bahman (1-2月)
12. Esfand (2-3月)

**ネパール暦 (Bikram Sambat):**
1. Baisakh (4-5月)
2. Jestha (5-6月)
3. Ashadh (6-7月)
4. Shrawan (7-8月)
5. Bhadra (8-9月)
6. Ashwin (9-10月)
7. Kartik (10-11月)
8. Mangsir (11-12月)
9. Poush (12-1月)
10. Magh (1-2月)
11. Falgun (2-3月)
12. Chaitra (3-4月)

**イスラム暦 (Hijri):**
1. Muharram
2. Safar
3. Rabi al-Awwal
4. Rabi al-Thani
5. Jumada al-Awwal
6. Jumada al-Thani
7. Rajab
8. Shaban
9. Ramadan
10. Shawwal
11. Dhu al-Qadah
12. Dhu al-Hijjah

## オンラインコンバーター

| サービス | URL |
|---------|-----|
| ペルシャ暦 | https://www.iranchamber.com/calendar/converter/iranian_calendar_converter.php |
| ネパール暦 | https://www.hamropatro.com/date-converter |
| イスラム暦 | https://www.islamicfinder.org/islamic-calendar/converter/ |
| エチオピア暦 | https://www.ethiopiancalendar.net/converter.html |

## 非ラテン数字の読み方

### ペルシャ語/アラビア語数字
| ۰ | ۱ | ۲ | ۳ | ۴ | ۵ | ۶ | ۷ | ۸ | ۹ |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |

### ネパール語（デーヴァナーガリー）数字
| ० | १ | २ | ३ | ४ | ५ | ६ | ७ | ८ | ९ |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |

### エチオピア数字（ゲエズ文字）
| ፩ | ፪ | ፫ | ፬ | ፭ | ፮ | ፯ | ፰ | ፱ | ፲ |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |

## 出力形式

```
## カレンダー変換

### 入力
- カレンダー: persian
- 日付: 1401 Esfand 2

### 結果

| カレンダー | 日付 |
|------------|------|
| Gregorian | 2023-02-21 |
| Persian | 1401 Esfand 2 |
| Islamic | 1444 Shaban 1 |
| Nepali | 2079 Falgun 9 |
| Ethiopian | 2015 Yekatit 14 |
```

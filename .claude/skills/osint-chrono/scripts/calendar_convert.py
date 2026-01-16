#!/usr/bin/env python3
"""
カレンダー変換ツール

複数のカレンダーシステム間で日付を変換する。
対応カレンダー:
- グレゴリオ暦 (Gregorian)
- ペルシャ暦/太陽暦ヒジュラ暦 (Persian/Jalali/Solar Hijri)
- イスラム暦/太陰暦ヒジュラ暦 (Islamic/Hijri/Lunar Hijri)
- ネパール暦/ビクラム・サンバト暦 (Nepali/Bikram Sambat)
- エチオピア暦 (Ethiopian) - 手動計算

使用例:
    python calendar_convert.py --from persian --to gregorian 1401 12 2
    python calendar_convert.py --from nepali --to gregorian 2072 10 17
    python calendar_convert.py --from islamic --to gregorian 1445 7 15
    python calendar_convert.py --from gregorian --to all 2023 2 21
"""

import argparse
import sys
from datetime import date, datetime
from typing import Optional, Tuple

# Persian calendar
try:
    import jdatetime
    PERSIAN_AVAILABLE = True
except ImportError:
    PERSIAN_AVAILABLE = False

# Islamic calendar
try:
    from hijri_converter import Hijri, Gregorian
    ISLAMIC_AVAILABLE = True
except ImportError:
    ISLAMIC_AVAILABLE = False

# Nepali calendar
try:
    import nepali_datetime
    NEPALI_AVAILABLE = True
except ImportError:
    NEPALI_AVAILABLE = False


# Ethiopian calendar constants
ETHIOPIAN_EPOCH_OFFSET_DAYS = 2796  # Days between Ethiopian and Gregorian epochs


def ethiopian_to_gregorian(year: int, month: int, day: int) -> date:
    """
    エチオピア暦からグレゴリオ暦に変換

    エチオピア暦:
    - 13ヶ月（12ヶ月×30日 + 1ヶ月×5-6日）
    - グレゴリオ暦より約7-8年遅れ
    - 新年は9月11日（うるう年は9月12日）
    """
    # エチオピア暦の日数を計算
    ethiopian_days = (year - 1) * 365 + (year // 4) + (month - 1) * 30 + day

    # グレゴリオ暦への変換
    # エチオピア元年1月1日 = グレゴリオ暦 AD 8年8月29日（ユリウス暦）
    # 簡易計算: グレゴリオ年 ≈ エチオピア年 + 7 or 8

    # より正確な計算
    jdn = ethiopian_days + 1723856  # Julian Day Number

    # JDNからグレゴリオ暦への変換
    l = jdn + 68569
    n = (4 * l) // 146097
    l = l - (146097 * n + 3) // 4
    i = (4000 * (l + 1)) // 1461001
    l = l - (1461 * i) // 4 + 31
    j = (80 * l) // 2447
    g_day = l - (2447 * j) // 80
    l = j // 11
    g_month = j + 2 - 12 * l
    g_year = 100 * (n - 49) + i + l

    return date(g_year, g_month, g_day)


def gregorian_to_ethiopian(g_date: date) -> Tuple[int, int, int]:
    """グレゴリオ暦からエチオピア暦に変換"""
    # Julian Day Numberを計算
    a = (14 - g_date.month) // 12
    y = g_date.year + 4800 - a
    m = g_date.month + 12 * a - 3
    jdn = g_date.day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045

    # エチオピア暦への変換
    ethiopian_days = jdn - 1723856

    # うるう年の計算
    year = (4 * ethiopian_days + 1463) // 1461
    day_of_year = ethiopian_days - (365 * year + year // 4) + 366

    if day_of_year <= 0:
        year -= 1
        day_of_year = ethiopian_days - (365 * year + year // 4) + 366

    month = (day_of_year - 1) // 30 + 1
    day = day_of_year - (month - 1) * 30

    return (year, month, day)


def persian_to_gregorian(year: int, month: int, day: int) -> Optional[date]:
    """ペルシャ暦（太陽暦ヒジュラ暦）からグレゴリオ暦に変換"""
    if not PERSIAN_AVAILABLE:
        print("Error: jdatetime library not installed", file=sys.stderr)
        return None

    j_date = jdatetime.date(year, month, day)
    g_date = j_date.togregorian()
    return g_date


def gregorian_to_persian(g_date: date) -> Optional[Tuple[int, int, int]]:
    """グレゴリオ暦からペルシャ暦に変換"""
    if not PERSIAN_AVAILABLE:
        return None

    j_date = jdatetime.date.fromgregorian(date=g_date)
    return (j_date.year, j_date.month, j_date.day)


def islamic_to_gregorian(year: int, month: int, day: int) -> Optional[date]:
    """イスラム暦（太陰暦ヒジュラ暦）からグレゴリオ暦に変換"""
    if not ISLAMIC_AVAILABLE:
        print("Error: hijri-converter library not installed", file=sys.stderr)
        return None

    hijri = Hijri(year, month, day)
    gregorian = hijri.to_gregorian()
    return date(gregorian.year, gregorian.month, gregorian.day)


def gregorian_to_islamic(g_date: date) -> Optional[Tuple[int, int, int]]:
    """グレゴリオ暦からイスラム暦に変換"""
    if not ISLAMIC_AVAILABLE:
        return None

    gregorian = Gregorian(g_date.year, g_date.month, g_date.day)
    hijri = gregorian.to_hijri()
    return (hijri.year, hijri.month, hijri.day)


def nepali_to_gregorian(year: int, month: int, day: int) -> Optional[date]:
    """ネパール暦（ビクラム・サンバト暦）からグレゴリオ暦に変換"""
    if not NEPALI_AVAILABLE:
        print("Error: nepali-datetime library not installed", file=sys.stderr)
        return None

    try:
        np_date = nepali_datetime.date(year, month, day)
        g_datetime = np_date.to_datetime_date()
        return g_datetime
    except Exception as e:
        print(f"Error converting Nepali date: {e}", file=sys.stderr)
        return None


def gregorian_to_nepali(g_date: date) -> Optional[Tuple[int, int, int]]:
    """グレゴリオ暦からネパール暦に変換"""
    if not NEPALI_AVAILABLE:
        return None

    try:
        np_date = nepali_datetime.date.from_datetime_date(g_date)
        return (np_date.year, np_date.month, np_date.day)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return None


# Month names for display
PERSIAN_MONTHS = [
    "Farvardin", "Ordibehesht", "Khordad", "Tir", "Mordad", "Shahrivar",
    "Mehr", "Aban", "Azar", "Dey", "Bahman", "Esfand"
]

ISLAMIC_MONTHS = [
    "Muharram", "Safar", "Rabi al-Awwal", "Rabi al-Thani",
    "Jumada al-Awwal", "Jumada al-Thani", "Rajab", "Shaban",
    "Ramadan", "Shawwal", "Dhu al-Qadah", "Dhu al-Hijjah"
]

NEPALI_MONTHS = [
    "Baisakh", "Jestha", "Ashadh", "Shrawan", "Bhadra", "Ashwin",
    "Kartik", "Mangsir", "Poush", "Magh", "Falgun", "Chaitra"
]

ETHIOPIAN_MONTHS = [
    "Meskerem", "Tikimt", "Hidar", "Tahsas", "Tir", "Yekatit",
    "Megabit", "Miyazya", "Ginbot", "Sene", "Hamle", "Nehase", "Pagume"
]


def format_date(calendar: str, year: int, month: int, day: int) -> str:
    """日付をフォーマットして表示"""
    if calendar == "gregorian":
        return f"{year}-{month:02d}-{day:02d}"
    elif calendar == "persian":
        month_name = PERSIAN_MONTHS[month - 1] if 1 <= month <= 12 else str(month)
        return f"{year} {month_name} {day}"
    elif calendar == "islamic":
        month_name = ISLAMIC_MONTHS[month - 1] if 1 <= month <= 12 else str(month)
        return f"{year} {month_name} {day}"
    elif calendar == "nepali":
        month_name = NEPALI_MONTHS[month - 1] if 1 <= month <= 12 else str(month)
        return f"{year} {month_name} {day}"
    elif calendar == "ethiopian":
        month_name = ETHIOPIAN_MONTHS[month - 1] if 1 <= month <= 13 else str(month)
        return f"{year} {month_name} {day}"
    return f"{year}-{month}-{day}"


def convert_to_gregorian(from_cal: str, year: int, month: int, day: int) -> Optional[date]:
    """指定されたカレンダーからグレゴリオ暦に変換"""
    if from_cal == "gregorian":
        return date(year, month, day)
    elif from_cal == "persian":
        return persian_to_gregorian(year, month, day)
    elif from_cal == "islamic":
        return islamic_to_gregorian(year, month, day)
    elif from_cal == "nepali":
        return nepali_to_gregorian(year, month, day)
    elif from_cal == "ethiopian":
        return ethiopian_to_gregorian(year, month, day)
    return None


def convert_from_gregorian(g_date: date, to_cal: str) -> Optional[Tuple[int, int, int]]:
    """グレゴリオ暦から指定されたカレンダーに変換"""
    if to_cal == "gregorian":
        return (g_date.year, g_date.month, g_date.day)
    elif to_cal == "persian":
        return gregorian_to_persian(g_date)
    elif to_cal == "islamic":
        return gregorian_to_islamic(g_date)
    elif to_cal == "nepali":
        return gregorian_to_nepali(g_date)
    elif to_cal == "ethiopian":
        return gregorian_to_ethiopian(g_date)
    return None


def main():
    parser = argparse.ArgumentParser(
        description="カレンダー変換ツール - 複数のカレンダーシステム間で日付を変換",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
対応カレンダー:
  gregorian  - グレゴリオ暦
  persian    - ペルシャ暦（太陽暦ヒジュラ暦/Jalali）
  islamic    - イスラム暦（太陰暦ヒジュラ暦）
  nepali     - ネパール暦（ビクラム・サンバト暦）
  ethiopian  - エチオピア暦

使用例:
  # ペルシャ暦 1401年12月2日 → グレゴリオ暦
  python calendar_convert.py --from persian --to gregorian 1401 12 2

  # ネパール暦 2072年10月17日 → グレゴリオ暦
  python calendar_convert.py --from nepali --to gregorian 2072 10 17

  # グレゴリオ暦 2023年2月21日 → 全カレンダー
  python calendar_convert.py --from gregorian --to all 2023 2 21
        """
    )

    parser.add_argument("--from", "-f", dest="from_cal", required=True,
                        choices=["gregorian", "persian", "islamic", "nepali", "ethiopian"],
                        help="変換元のカレンダー")
    parser.add_argument("--to", "-t", dest="to_cal", required=True,
                        choices=["gregorian", "persian", "islamic", "nepali", "ethiopian", "all"],
                        help="変換先のカレンダー（'all'で全て表示）")
    parser.add_argument("year", type=int, help="年")
    parser.add_argument("month", type=int, help="月")
    parser.add_argument("day", type=int, help="日")

    args = parser.parse_args()

    # Check library availability
    print("## カレンダー変換\n")

    # 入力表示
    print(f"### 入力")
    print(f"- カレンダー: {args.from_cal}")
    print(f"- 日付: {format_date(args.from_cal, args.year, args.month, args.day)}")
    print()

    # まずグレゴリオ暦に変換
    g_date = convert_to_gregorian(args.from_cal, args.year, args.month, args.day)

    if g_date is None:
        print("Error: 変換に失敗しました", file=sys.stderr)
        sys.exit(1)

    print(f"### 結果\n")

    if args.to_cal == "all":
        # 全カレンダーに変換
        calendars = ["gregorian", "persian", "islamic", "nepali", "ethiopian"]
        print("| カレンダー | 日付 |")
        print("|------------|------|")

        for cal in calendars:
            result = convert_from_gregorian(g_date, cal)
            if result:
                formatted = format_date(cal, *result)
                print(f"| {cal.capitalize()} | {formatted} |")
            else:
                print(f"| {cal.capitalize()} | (ライブラリ未インストール) |")
    else:
        # 特定のカレンダーに変換
        result = convert_from_gregorian(g_date, args.to_cal)
        if result:
            formatted = format_date(args.to_cal, *result)
            print(f"**{args.to_cal.capitalize()}:** {formatted}")
        else:
            print(f"Error: {args.to_cal}への変換に失敗しました", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()

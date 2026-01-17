#!/usr/bin/env python3
"""
影の角度計算ツール（Chronolocation）

太陽位置から影の角度を計算、または影の角度から撮影時刻を推定する。

使用例:
    # 特定の日時・場所での太陽位置と影の方向を計算
    python shadow_calc.py --lat 35.6812 --lon 139.7671 --date 2024-06-15 --time 14:30

    # 影の角度から撮影時刻を推定
    python shadow_calc.py --lat 35.6812 --lon 139.7671 --date 2024-06-15 --shadow-azimuth 45

    # 1日の太陽軌道を表示
    python shadow_calc.py --lat 35.6812 --lon 139.7671 --date 2024-06-15 --all-day
"""

import argparse
import math
import sys
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple, List

try:
    import pytz
    PYTZ_AVAILABLE = True
except ImportError:
    PYTZ_AVAILABLE = False


def calculate_julian_day(year: int, month: int, day: int, hour: float = 12.0) -> float:
    """ユリウス日を計算"""
    if month <= 2:
        year -= 1
        month += 12

    A = int(year / 100)
    B = 2 - A + int(A / 4)

    JD = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + B - 1524.5 + hour / 24.0
    return JD


def calculate_sun_position(lat: float, lon: float, dt: datetime) -> Tuple[float, float]:
    """
    太陽の位置（方位角と高度）を計算

    Returns:
        (azimuth, altitude): 方位角（北=0°、東=90°）、高度（水平=0°）
    """
    # UTC時刻に変換
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)

    # ユリウス日
    hour = dt.hour + dt.minute / 60.0 + dt.second / 3600.0
    JD = calculate_julian_day(dt.year, dt.month, dt.day, hour)

    # ユリウス世紀
    T = (JD - 2451545.0) / 36525.0

    # 太陽の幾何学的平均黄経
    L0 = (280.46646 + T * (36000.76983 + 0.0003032 * T)) % 360

    # 太陽の平均近点角
    M = (357.52911 + T * (35999.05029 - 0.0001537 * T)) % 360
    M_rad = math.radians(M)

    # 離心率
    e = 0.016708634 - T * (0.000042037 + 0.0000001267 * T)

    # 太陽の中心方程式
    C = (1.914602 - T * (0.004817 + 0.000014 * T)) * math.sin(M_rad)
    C += (0.019993 - 0.000101 * T) * math.sin(2 * M_rad)
    C += 0.000289 * math.sin(3 * M_rad)

    # 太陽の真黄経
    sun_lon = L0 + C

    # 黄道傾斜角
    obliquity = 23.439291 - 0.0130042 * T
    obliquity_rad = math.radians(obliquity)

    # 太陽の赤経・赤緯
    sun_lon_rad = math.radians(sun_lon)
    RA = math.atan2(
        math.cos(obliquity_rad) * math.sin(sun_lon_rad),
        math.cos(sun_lon_rad)
    )
    dec = math.asin(math.sin(obliquity_rad) * math.sin(sun_lon_rad))

    # 恒星時
    GMST = (280.46061837 + 360.98564736629 * (JD - 2451545.0) +
            0.000387933 * T * T - T * T * T / 38710000.0) % 360
    LMST = math.radians((GMST + lon) % 360)

    # 時角
    HA = LMST - RA

    # 高度と方位角
    lat_rad = math.radians(lat)

    altitude = math.asin(
        math.sin(lat_rad) * math.sin(dec) +
        math.cos(lat_rad) * math.cos(dec) * math.cos(HA)
    )

    azimuth = math.atan2(
        -math.sin(HA),
        math.tan(dec) * math.cos(lat_rad) - math.sin(lat_rad) * math.cos(HA)
    )

    # 度に変換、方位角を北基準に調整
    altitude_deg = math.degrees(altitude)
    azimuth_deg = (math.degrees(azimuth) + 360) % 360

    return azimuth_deg, altitude_deg


def calculate_shadow_direction(sun_azimuth: float) -> float:
    """太陽の方位角から影の方向を計算（影は太陽の反対方向）"""
    return (sun_azimuth + 180) % 360


def calculate_shadow_length_ratio(sun_altitude: float) -> Optional[float]:
    """
    太陽高度から影の長さ比率を計算

    Returns:
        物体の高さに対する影の長さの比率（太陽が水平以下なら None）
    """
    if sun_altitude <= 0:
        return None

    return 1 / math.tan(math.radians(sun_altitude))


def estimate_time_from_shadow(
    lat: float,
    lon: float,
    date: datetime,
    shadow_azimuth: float,
    tolerance: float = 5.0
) -> List[Tuple[datetime, float]]:
    """
    影の方位角から撮影時刻を推定

    Args:
        shadow_azimuth: 影の方位角（北=0°）
        tolerance: 許容誤差（度）

    Returns:
        List of (datetime, sun_altitude) tuples
    """
    results = []

    # 日の出から日の入りまで5分刻みでスキャン
    for minutes in range(0, 24 * 60, 5):
        check_time = datetime(date.year, date.month, date.day, 0, 0, tzinfo=timezone.utc)
        check_time += timedelta(minutes=minutes)

        sun_az, sun_alt = calculate_sun_position(lat, lon, check_time)

        # 太陽が地平線以下なら無視
        if sun_alt < 0:
            continue

        # 影の方向を計算
        calc_shadow_az = calculate_shadow_direction(sun_az)

        # 差を計算（360度の循環を考慮）
        diff = abs(calc_shadow_az - shadow_azimuth)
        if diff > 180:
            diff = 360 - diff

        if diff <= tolerance:
            results.append((check_time, sun_alt))

    return results


def azimuth_to_compass(azimuth: float) -> str:
    """方位角を16方位に変換"""
    directions = [
        "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
    ]
    index = int((azimuth + 11.25) / 22.5) % 16
    return directions[index]


def main():
    parser = argparse.ArgumentParser(
        description="影の角度計算ツール - 太陽位置と影の方向を計算",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 特定日時の太陽位置を計算
  python shadow_calc.py --lat 35.6812 --lon 139.7671 --date 2024-06-15 --time 14:30

  # 影の方向から時刻を推定（影が北東=45°を指している場合）
  python shadow_calc.py --lat 35.6812 --lon 139.7671 --date 2024-06-15 --shadow-azimuth 45

  # 1日の太陽軌道を表示
  python shadow_calc.py --lat 35.6812 --lon 139.7671 --date 2024-06-15 --all-day

  # SunCalcへのリンクを生成
  python shadow_calc.py --lat 35.6812 --lon 139.7671 --date 2024-06-15 --suncalc

方位角の基準:
  北=0°, 東=90°, 南=180°, 西=270°
        """
    )

    parser.add_argument("--lat", type=float, required=True, help="緯度")
    parser.add_argument("--lon", type=float, required=True, help="経度")
    parser.add_argument("--date", required=True, help="日付（YYYY-MM-DD形式）")
    parser.add_argument("--time", help="時刻（HH:MM形式、UTC）")
    parser.add_argument("--shadow-azimuth", type=float, help="影の方位角（北=0°）から時刻を推定")
    parser.add_argument("--all-day", action="store_true", help="1日の太陽軌道を表示")
    parser.add_argument("--suncalc", action="store_true", help="SunCalcへのリンクを生成")
    parser.add_argument("--tz", help="タイムゾーン（例: Asia/Tokyo）")

    args = parser.parse_args()

    # 日付パース
    try:
        date = datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError:
        print(f"Error: 日付形式が不正です: {args.date}（YYYY-MM-DD形式で指定）", file=sys.stderr)
        sys.exit(1)

    print("## 影の角度計算（Chronolocation）\n")

    print("### 入力条件")
    print(f"- 座標: {args.lat}, {args.lon}")
    print(f"- 日付: {args.date}")

    # タイムゾーン処理
    tz = None
    if args.tz and PYTZ_AVAILABLE:
        try:
            tz = pytz.timezone(args.tz)
            print(f"- タイムゾーン: {args.tz}")
        except Exception:
            print(f"- タイムゾーン: UTC（{args.tz}は無効）")
    else:
        print("- タイムゾーン: UTC")
    print()

    # SunCalcリンク
    if args.suncalc:
        suncalc_url = f"https://www.suncalc.org/#/{args.lat},{args.lon},15/{args.date}/1200/1/3"
        print(f"### SunCalc")
        print(f"{suncalc_url}")
        print()

    # 影の方位角から時刻を推定
    if args.shadow_azimuth is not None:
        print(f"### 時刻推定（影の方位角: {args.shadow_azimuth}°）")

        results = estimate_time_from_shadow(args.lat, args.lon, date, args.shadow_azimuth)

        if not results:
            print("\n該当する時刻が見つかりませんでした。")
            print("（影の方向が指定の方位角になる時刻がこの日にはない可能性があります）")
        else:
            print("\n| 時刻 (UTC) | 太陽高度 | 太陽方位 | 影の長さ比 |")
            print("|------------|----------|----------|------------|")

            for dt, sun_alt in results:
                sun_az, _ = calculate_sun_position(args.lat, args.lon, dt)
                shadow_ratio = calculate_shadow_length_ratio(sun_alt)
                ratio_str = f"{shadow_ratio:.2f}x" if shadow_ratio else "N/A"

                local_time = dt
                if tz:
                    local_time = dt.astimezone(tz)
                    time_str = f"{local_time.strftime('%H:%M')} ({args.tz})"
                else:
                    time_str = f"{dt.strftime('%H:%M')} UTC"

                print(f"| {time_str} | {sun_alt:.1f}° | {sun_az:.1f}° ({azimuth_to_compass(sun_az)}) | {ratio_str} |")
        print()
        return

    # 特定時刻の太陽位置
    if args.time:
        try:
            time_parts = args.time.split(":")
            hour, minute = int(time_parts[0]), int(time_parts[1])
            dt = datetime(date.year, date.month, date.day, hour, minute, tzinfo=timezone.utc)
        except (ValueError, IndexError):
            print(f"Error: 時刻形式が不正です: {args.time}（HH:MM形式で指定）", file=sys.stderr)
            sys.exit(1)

        sun_az, sun_alt = calculate_sun_position(args.lat, args.lon, dt)
        shadow_az = calculate_shadow_direction(sun_az)
        shadow_ratio = calculate_shadow_length_ratio(sun_alt)

        print(f"### 太陽位置（{args.time} UTC）")
        print(f"- 方位角: {sun_az:.1f}° ({azimuth_to_compass(sun_az)})")
        print(f"- 高度: {sun_alt:.1f}°")
        print()

        print("### 影の情報")
        print(f"- 方向: {shadow_az:.1f}° ({azimuth_to_compass(shadow_az)})")
        if shadow_ratio:
            print(f"- 長さ比: {shadow_ratio:.2f}x（物体高さの{shadow_ratio:.2f}倍）")
        else:
            print("- 長さ比: N/A（太陽が地平線以下）")
        print()
        return

    # 1日の太陽軌道
    if args.all_day:
        print("### 1日の太陽軌道")
        print("\n| 時刻 | 方位角 | 高度 | 影の方向 | 影の長さ比 |")
        print("|------|--------|------|----------|------------|")

        for hour in range(0, 24):
            dt = datetime(date.year, date.month, date.day, hour, 0, tzinfo=timezone.utc)
            sun_az, sun_alt = calculate_sun_position(args.lat, args.lon, dt)

            if sun_alt < -5:  # 日の出前・日の入り後は省略
                continue

            shadow_az = calculate_shadow_direction(sun_az)
            shadow_ratio = calculate_shadow_length_ratio(sun_alt)
            ratio_str = f"{shadow_ratio:.2f}x" if shadow_ratio else "-"

            alt_indicator = "" if sun_alt > 0 else " (below horizon)"
            print(f"| {hour:02d}:00 | {sun_az:.1f}° ({azimuth_to_compass(sun_az)}) | {sun_alt:.1f}°{alt_indicator} | {shadow_az:.1f}° ({azimuth_to_compass(shadow_az)}) | {ratio_str} |")
        print()
        return

    # デフォルト: 正午の太陽位置
    dt = datetime(date.year, date.month, date.day, 12, 0, tzinfo=timezone.utc)
    sun_az, sun_alt = calculate_sun_position(args.lat, args.lon, dt)
    shadow_az = calculate_shadow_direction(sun_az)

    print("### 正午（12:00 UTC）の太陽位置")
    print(f"- 方位角: {sun_az:.1f}° ({azimuth_to_compass(sun_az)})")
    print(f"- 高度: {sun_alt:.1f}°")
    print(f"- 影の方向: {shadow_az:.1f}° ({azimuth_to_compass(shadow_az)})")
    print()
    print("**ヒント**: `--time` で特定時刻、`--all-day` で1日の軌道、")
    print("`--shadow-azimuth` で影の方向から時刻を推定できます。")


if __name__ == "__main__":
    main()

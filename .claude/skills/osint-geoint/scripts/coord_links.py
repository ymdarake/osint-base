#!/usr/bin/env python3
"""
座標からOSINTに有用なリンクを一括生成するスクリプト。

Usage:
    python coord_links.py <lat> <lon>
    python coord_links.py 41.352757 -4.690017
"""

import sys
import urllib.parse


def generate_links(lat: float, lon: float) -> dict:
    """座標から各種マップサービスのリンクを生成"""
    return {
        "Google Maps": f"https://maps.google.com/?q={lat},{lon}",
        "Google Earth": f"https://earth.google.com/web/@{lat},{lon},500a,35y,0h,0t,0r",
        "OpenStreetMap": f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}&zoom=15",
        "Yandex Maps": f"https://yandex.com/maps/?ll={lon},{lat}&z=15&pt={lon},{lat}",
        "Bing Maps": f"https://www.bing.com/maps?cp={lat}~{lon}&lvl=15",
        "what3words": f"https://what3words.com/{lat},{lon}",
        "SunCalc": f"https://www.suncalc.org/#/{lat},{lon},15/null/null/null/null",
        "Sentinel Hub": f"https://apps.sentinel-hub.com/eo-browser/?zoom=14&lat={lat}&lng={lon}",
        "Overpass Turbo": f"https://overpass-turbo.eu/?lat={lat}&lon={lon}&zoom=15",
    }


def format_coordinates(lat: float, lon: float) -> dict:
    """座標を各種形式に変換"""
    # DMS (度分秒) 形式
    def dd_to_dms(dd, is_lat=True):
        direction = ("N" if dd >= 0 else "S") if is_lat else ("E" if dd >= 0 else "W")
        dd = abs(dd)
        d = int(dd)
        m = int((dd - d) * 60)
        s = (dd - d - m / 60) * 3600
        return f"{d}°{m}'{s:.2f}\"{direction}"

    lat_dms = dd_to_dms(lat, is_lat=True)
    lon_dms = dd_to_dms(lon, is_lat=False)

    return {
        "Decimal (DD)": f"{lat}, {lon}",
        "DMS": f"{lat_dms} {lon_dms}",
        "Google Search": f"{lat}, {lon}",
    }


def main():
    if len(sys.argv) != 3:
        print("Usage: python coord_links.py <lat> <lon>")
        print("Example: python coord_links.py 41.352757 -4.690017")
        sys.exit(1)

    try:
        lat = float(sys.argv[1])
        lon = float(sys.argv[2])
    except ValueError:
        print("Error: Invalid coordinates. Please provide numeric values.")
        sys.exit(1)

    print(f"## 座標: {lat}, {lon}\n")

    print("### 座標形式")
    for name, value in format_coordinates(lat, lon).items():
        print(f"- **{name}**: {value}")

    print("\n### マップリンク")
    for name, url in generate_links(lat, lon).items():
        print(f"- [{name}]({url})")


if __name__ == "__main__":
    main()

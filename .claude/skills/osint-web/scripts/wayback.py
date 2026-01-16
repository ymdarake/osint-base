#!/usr/bin/env python3
"""
Wayback Machine APIを使用してアーカイブ情報を取得するスクリプト。

Usage:
    python wayback.py <url>                    # 最新のアーカイブを取得
    python wayback.py <url> --list             # 全アーカイブ一覧
    python wayback.py <url> --date 20230101    # 特定日付のアーカイブ
"""

import sys
import json
import urllib.request
import urllib.parse
from datetime import datetime


def get_available_snapshots(url: str) -> dict:
    """Wayback Machine APIで利用可能なスナップショットを取得"""
    api_url = f"https://archive.org/wayback/available?url={urllib.parse.quote(url)}"
    try:
        with urllib.request.urlopen(api_url, timeout=10) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        return {"error": str(e)}


def get_cdx_snapshots(url: str, limit: int = 20) -> list:
    """CDX APIで全スナップショット一覧を取得"""
    cdx_url = f"https://web.archive.org/cdx/search/cdx?url={urllib.parse.quote(url)}&output=json&limit={limit}"
    try:
        with urllib.request.urlopen(cdx_url, timeout=15) as response:
            data = json.loads(response.read().decode())
            if len(data) > 1:
                headers = data[0]
                return [dict(zip(headers, row)) for row in data[1:]]
            return []
    except Exception as e:
        return [{"error": str(e)}]


def format_wayback_url(url: str, timestamp: str) -> str:
    """Wayback Machine URLを生成"""
    return f"https://web.archive.org/web/{timestamp}/{url}"


def main():
    if len(sys.argv) < 2:
        print("Usage: python wayback.py <url> [--list] [--date YYYYMMDD]")
        print("\nExamples:")
        print("  python wayback.py https://example.com")
        print("  python wayback.py https://example.com --list")
        print("  python wayback.py https://example.com --date 20230615")
        sys.exit(1)

    url = sys.argv[1]
    list_mode = "--list" in sys.argv
    date_mode = "--date" in sys.argv

    print(f"## Wayback Machine: {url}\n")

    if list_mode:
        print("### アーカイブ一覧（最新20件）\n")
        snapshots = get_cdx_snapshots(url)
        if snapshots and "error" not in snapshots[0]:
            print("| 日時 | ステータス | リンク |")
            print("|------|----------|--------|")
            for snap in snapshots:
                ts = snap.get("timestamp", "")
                status = snap.get("statuscode", "")
                if ts:
                    formatted_date = f"{ts[:4]}-{ts[4:6]}-{ts[6:8]} {ts[8:10]}:{ts[10:12]}"
                    archive_url = format_wayback_url(url, ts)
                    print(f"| {formatted_date} | {status} | [開く]({archive_url}) |")
        else:
            print("アーカイブが見つかりませんでした。")

    elif date_mode:
        date_idx = sys.argv.index("--date")
        if date_idx + 1 < len(sys.argv):
            target_date = sys.argv[date_idx + 1]
            archive_url = format_wayback_url(url, target_date)
            print(f"### 指定日付のアーカイブ\n")
            print(f"- 日付: {target_date}")
            print(f"- URL: {archive_url}")
        else:
            print("Error: --date requires a date argument (YYYYMMDD)")

    else:
        print("### 最新のアーカイブ\n")
        result = get_available_snapshots(url)
        if "archived_snapshots" in result:
            closest = result["archived_snapshots"].get("closest", {})
            if closest:
                ts = closest.get("timestamp", "")
                archive_url = closest.get("url", "")
                available = closest.get("available", False)
                status = closest.get("status", "")

                if ts:
                    formatted_date = f"{ts[:4]}-{ts[4:6]}-{ts[6:8]} {ts[8:10]}:{ts[10:12]}"
                else:
                    formatted_date = "不明"

                print(f"- 日時: {formatted_date}")
                print(f"- ステータス: {status}")
                print(f"- URL: {archive_url}")
            else:
                print("アーカイブが見つかりませんでした。")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    main()

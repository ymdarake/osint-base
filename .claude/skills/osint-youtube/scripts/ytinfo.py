#!/usr/bin/env python3
"""
YouTube動画の情報を取得するスクリプト（yt-dlp使用）。

Usage:
    python ytinfo.py <youtube_url>                    # 基本情報
    python ytinfo.py <youtube_url> --subtitles        # 字幕一覧
    python ytinfo.py <youtube_url> --download-subs    # 字幕をダウンロード
"""

import sys
import subprocess
import json


def get_video_info(url: str) -> dict:
    """yt-dlpで動画情報を取得"""
    try:
        result = subprocess.run(
            ["yt-dlp", "-j", "--no-download", url],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            return {"error": result.stderr}
    except FileNotFoundError:
        return {"error": "yt-dlp not installed. Run: pip install yt-dlp"}
    except Exception as e:
        return {"error": str(e)}


def list_subtitles(url: str) -> dict:
    """利用可能な字幕を一覧"""
    try:
        result = subprocess.run(
            ["yt-dlp", "--list-subs", "--no-download", url],
            capture_output=True,
            text=True,
            timeout=30
        )
        return {"output": result.stdout, "error": result.stderr if result.returncode != 0 else None}
    except Exception as e:
        return {"error": str(e)}


def download_subtitles(url: str, output_dir: str = ".") -> dict:
    """字幕をダウンロード"""
    try:
        result = subprocess.run(
            [
                "yt-dlp",
                "--write-auto-sub",
                "--write-sub",
                "--sub-lang", "en,ja,es,pt,fr,de,zh,ko,ru,ar",
                "--sub-format", "srt/vtt/best",
                "--skip-download",
                "-o", f"{output_dir}/%(title)s.%(ext)s",
                url
            ],
            capture_output=True,
            text=True,
            timeout=60
        )
        return {"output": result.stdout, "error": result.stderr if result.returncode != 0 else None}
    except Exception as e:
        return {"error": str(e)}


def main():
    if len(sys.argv) < 2:
        print("Usage: python ytinfo.py <youtube_url> [--subtitles] [--download-subs]")
        print("\nExamples:")
        print("  python ytinfo.py https://youtu.be/abc123")
        print("  python ytinfo.py https://youtu.be/abc123 --subtitles")
        print("  python ytinfo.py https://youtu.be/abc123 --download-subs")
        sys.exit(1)

    url = sys.argv[1]
    subtitles_mode = "--subtitles" in sys.argv
    download_mode = "--download-subs" in sys.argv

    if subtitles_mode:
        print(f"## 字幕一覧: {url}\n")
        result = list_subtitles(url)
        if result.get("output"):
            print(result["output"])
        if result.get("error"):
            print(f"Error: {result['error']}")

    elif download_mode:
        print(f"## 字幕ダウンロード: {url}\n")
        result = download_subtitles(url)
        if result.get("output"):
            print(result["output"])
        if result.get("error"):
            print(f"Error: {result['error']}")
        else:
            print("字幕ファイルがダウンロードされました。")

    else:
        print(f"## YouTube動画情報\n")
        info = get_video_info(url)

        if "error" in info:
            print(f"Error: {info['error']}")
            sys.exit(1)

        print(f"### 基本情報\n")
        print(f"- **タイトル:** {info.get('title', 'N/A')}")
        print(f"- **チャンネル:** {info.get('channel', 'N/A')}")
        print(f"- **アップロード日:** {info.get('upload_date', 'N/A')}")
        print(f"- **長さ:** {info.get('duration_string', 'N/A')}")
        print(f"- **再生回数:** {info.get('view_count', 'N/A'):,}")
        print(f"- **説明:**")
        desc = info.get('description', '')
        if desc:
            # 最初の500文字のみ表示
            print(f"  {desc[:500]}{'...' if len(desc) > 500 else ''}")

        print(f"\n### メタデータ\n")
        print(f"- **ID:** {info.get('id', 'N/A')}")
        print(f"- **カテゴリ:** {', '.join(info.get('categories', []))}")
        print(f"- **タグ:** {', '.join(info.get('tags', [])[:10])}")

        # 字幕情報
        subtitles = info.get('subtitles', {})
        auto_subs = info.get('automatic_captions', {})
        if subtitles or auto_subs:
            print(f"\n### 字幕\n")
            if subtitles:
                print(f"- **手動字幕:** {', '.join(subtitles.keys())}")
            if auto_subs:
                print(f"- **自動字幕:** {', '.join(list(auto_subs.keys())[:5])}...")


if __name__ == "__main__":
    main()

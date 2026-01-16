#!/usr/bin/env python3
"""
OSINT Image Analyzer
画像からメタデータとOCRテキストを抽出する
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_exiftool(image_path: str) -> dict:
    """exiftoolでメタデータを抽出"""
    try:
        result = subprocess.run(
            ["exiftool", "-json", image_path],
            capture_output=True,
            text=True,
            check=True
        )
        import json
        data = json.loads(result.stdout)
        return data[0] if data else {}
    except subprocess.CalledProcessError:
        return {"error": "exiftool failed"}
    except FileNotFoundError:
        return {"error": "exiftool not installed"}


def run_ocr(image_path: str, lang: str = "eng") -> str:
    """tesseractでOCRを実行"""
    try:
        result = subprocess.run(
            ["tesseract", image_path, "stdout", "-l", lang],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"OCR error: {e.stderr}"
    except FileNotFoundError:
        return "tesseract not installed"


def format_gps(metadata: dict) -> str:
    """GPS座標をフォーマット"""
    lat = metadata.get("GPSLatitude")
    lon = metadata.get("GPSLongitude")
    lat_ref = metadata.get("GPSLatitudeRef", "N")
    lon_ref = metadata.get("GPSLongitudeRef", "E")

    if lat and lon:
        return f"{lat} {lat_ref}, {lon} {lon_ref}"
    return "Not available"


def analyze_image(image_path: str, lang: str = "eng") -> None:
    """画像を分析して結果を出力"""
    path = Path(image_path)
    if not path.exists():
        print(f"Error: File not found: {image_path}")
        sys.exit(1)

    print(f"## 画像分析結果: {path.name}\n")

    # メタデータ抽出
    print("### メタデータ")
    metadata = run_exiftool(image_path)

    if "error" in metadata:
        print(f"Error: {metadata['error']}")
    else:
        print(f"- **GPS**: {format_gps(metadata)}")
        print(f"- **撮影日時**: {metadata.get('CreateDate', metadata.get('DateTimeOriginal', 'N/A'))}")
        print(f"- **カメラ**: {metadata.get('Make', 'N/A')} {metadata.get('Model', '')}")
        print(f"- **ソフトウェア**: {metadata.get('Software', 'N/A')}")
        print(f"- **画像サイズ**: {metadata.get('ImageWidth', 'N/A')}x{metadata.get('ImageHeight', 'N/A')}")

    print()

    # OCR
    print("### OCRテキスト")
    ocr_text = run_ocr(image_path, lang)
    if ocr_text:
        print(f"```\n{ocr_text}\n```")
    else:
        print("テキストは検出されませんでした")

    print()

    # Google Maps リンク
    lat = metadata.get("GPSLatitude")
    lon = metadata.get("GPSLongitude")
    if lat and lon:
        # 度分秒を10進数に変換（簡易版）
        print("### 地図リンク")
        print(f"- exiftoolの座標をGoogle Mapsで確認してください")


def main():
    parser = argparse.ArgumentParser(description="OSINT Image Analyzer")
    parser.add_argument("image", help="分析する画像ファイルのパス")
    parser.add_argument("--lang", default="eng", help="OCR言語 (例: jpn+eng)")

    args = parser.parse_args()
    analyze_image(args.image, args.lang)


if __name__ == "__main__":
    main()

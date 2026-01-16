#!/usr/bin/env python3
"""
OSINT Video Frame Extractor
動画からフレームを抽出し、オプションでOCRを実行する
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def get_video_info(video_path: str) -> dict:
    """ffprobeで動画情報を取得"""
    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "quiet",
                "-print_format", "json",
                "-show_format", "-show_streams",
                video_path
            ],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError:
        return {"error": "ffprobe failed"}
    except FileNotFoundError:
        return {"error": "ffprobe not installed"}


def extract_frames(video_path: str, output_dir: str, interval: int) -> list:
    """動画からフレームを抽出"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    output_pattern = str(Path(output_dir) / "frame_%04d.png")

    try:
        subprocess.run(
            [
                "ffmpeg", "-i", video_path,
                "-vf", f"fps=1/{interval}",
                "-y",  # 上書き許可
                output_pattern
            ],
            capture_output=True,
            check=True
        )

        # 抽出されたフレームをリスト
        frames = sorted(Path(output_dir).glob("frame_*.png"))
        return [str(f) for f in frames]

    except subprocess.CalledProcessError as e:
        print(f"Error extracting frames: {e.stderr.decode()}")
        return []
    except FileNotFoundError:
        print("Error: ffmpeg not installed")
        return []


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
    except subprocess.CalledProcessError:
        return ""
    except FileNotFoundError:
        return ""


def format_duration(seconds: float) -> str:
    """秒数を HH:MM:SS 形式に変換"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def analyze_video(video_path: str, output_dir: str, interval: int,
                  do_ocr: bool, lang: str) -> None:
    """動画を分析"""
    path = Path(video_path)
    if not path.exists():
        print(f"Error: File not found: {video_path}")
        sys.exit(1)

    print(f"## 動画分析結果: {path.name}\n")

    # メタデータ取得
    print("### メタデータ")
    info = get_video_info(video_path)

    if "error" in info:
        print(f"Error: {info['error']}")
    else:
        fmt = info.get("format", {})
        duration = float(fmt.get("duration", 0))
        print(f"- **長さ**: {format_duration(duration)}")

        # ビデオストリーム情報
        for stream in info.get("streams", []):
            if stream.get("codec_type") == "video":
                print(f"- **解像度**: {stream.get('width')}x{stream.get('height')}")
                print(f"- **コーデック**: {stream.get('codec_name')}")
                break

        creation_time = fmt.get("tags", {}).get("creation_time", "N/A")
        print(f"- **作成日時**: {creation_time}")

    print()

    # フレーム抽出
    print("### フレーム抽出")
    print(f"間隔: {interval}秒ごと")
    print(f"出力先: {output_dir}/")
    print()

    frames = extract_frames(video_path, output_dir, interval)
    print(f"抽出フレーム数: {len(frames)}")

    for i, frame in enumerate(frames):
        timestamp = format_duration(i * interval)
        print(f"- {Path(frame).name} ({timestamp})")

    print()

    # OCR
    if do_ocr and frames:
        print("### OCR結果")
        for frame in frames:
            text = run_ocr(frame, lang)
            if text:
                print(f"\n**{Path(frame).name}:**")
                print(f"```\n{text}\n```")


def main():
    parser = argparse.ArgumentParser(description="OSINT Video Frame Extractor")
    parser.add_argument("video", help="分析する動画ファイルのパス")
    parser.add_argument("--interval", type=int, default=5,
                        help="フレーム抽出間隔（秒）")
    parser.add_argument("--output", default="./frames",
                        help="出力ディレクトリ")
    parser.add_argument("--ocr", action="store_true",
                        help="各フレームでOCRを実行")
    parser.add_argument("--lang", default="eng",
                        help="OCR言語 (例: jpn+eng)")

    args = parser.parse_args()
    analyze_video(args.video, args.output, args.interval, args.ocr, args.lang)


if __name__ == "__main__":
    main()

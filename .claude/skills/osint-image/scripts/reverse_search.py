#!/usr/bin/env python3
"""
逆画像検索ツール

画像ファイルから各種逆画像検索サービスの検索URLを生成する。
また、画像のハッシュ値を計算してTinEye等での検索に使用可能。

使用例:
    python reverse_search.py /path/to/image.jpg
    python reverse_search.py /path/to/image.jpg --upload
    python reverse_search.py /path/to/image.jpg --hash-only
"""

import argparse
import base64
import hashlib
import os
import sys
import urllib.parse
from pathlib import Path
from typing import Optional

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


def calculate_image_hashes(image_path: str) -> dict:
    """画像のハッシュ値を計算"""
    hashes = {}

    with open(image_path, 'rb') as f:
        content = f.read()
        hashes['md5'] = hashlib.md5(content).hexdigest()
        hashes['sha256'] = hashlib.sha256(content).hexdigest()

    return hashes


def get_image_info(image_path: str) -> dict:
    """画像の基本情報を取得"""
    info = {
        'filename': os.path.basename(image_path),
        'size_bytes': os.path.getsize(image_path),
        'extension': Path(image_path).suffix.lower()
    }

    if PIL_AVAILABLE:
        try:
            with Image.open(image_path) as img:
                info['width'] = img.width
                info['height'] = img.height
                info['format'] = img.format
                info['mode'] = img.mode
        except Exception as e:
            info['pil_error'] = str(e)

    return info


def generate_search_urls(image_path: str, image_url: Optional[str] = None) -> dict:
    """逆画像検索サービスのURLを生成"""
    urls = {}

    # URL指定がある場合はそのURLを使用
    if image_url:
        encoded_url = urllib.parse.quote(image_url, safe='')

        urls['google_lens'] = f"https://lens.google.com/uploadbyurl?url={encoded_url}"
        urls['google_images'] = f"https://www.google.com/searchbyimage?image_url={encoded_url}"
        urls['yandex'] = f"https://yandex.com/images/search?url={encoded_url}&rpt=imageview"
        urls['bing'] = f"https://www.bing.com/images/search?view=detailv2&iss=sbi&q=imgurl:{encoded_url}"
        urls['tineye'] = f"https://tineye.com/search?url={encoded_url}"

    # 常に表示するマニュアル検索URL
    urls['google_images_upload'] = "https://images.google.com/ (カメラアイコンから画像をアップロード)"
    urls['yandex_upload'] = "https://yandex.com/images/ (カメラアイコンから画像をアップロード)"
    urls['tineye_upload'] = "https://tineye.com/ (画像をアップロード)"
    urls['bing_upload'] = "https://www.bing.com/visualsearch (画像をアップロード)"

    # 特殊用途の検索エンジン
    urls['pimeyes'] = "https://pimeyes.com/ (顔認識専用 - 有料)"
    urls['facecheck'] = "https://facecheck.id/ (顔認識)"
    urls['search4faces'] = "https://search4faces.com/ (SNS顔検索)"
    urls['karmadecay'] = "https://karmadecay.com/ (Reddit専用)"

    return urls


def upload_to_imgbb(image_path: str, api_key: Optional[str] = None) -> Optional[str]:
    """imgbbに画像をアップロードしてURLを取得"""
    if not REQUESTS_AVAILABLE:
        return None

    # 環境変数からAPIキーを取得
    if not api_key:
        api_key = os.environ.get('IMGBB_API_KEY')

    if not api_key:
        return None

    try:
        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')

        response = requests.post(
            'https://api.imgbb.com/1/upload',
            data={
                'key': api_key,
                'image': image_data
            },
            timeout=30
        )

        if response.status_code == 200:
            return response.json()['data']['url']
    except Exception:
        pass

    return None


def main():
    parser = argparse.ArgumentParser(
        description="逆画像検索ツール - 各種検索サービスのURLを生成",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 基本的な使用方法
  python reverse_search.py image.jpg

  # 画像URLがある場合（検索URLを直接生成）
  python reverse_search.py image.jpg --url https://example.com/image.jpg

  # ハッシュ値のみ表示
  python reverse_search.py image.jpg --hash-only

  # imgbbにアップロードして検索URL生成
  IMGBB_API_KEY=xxx python reverse_search.py image.jpg --upload
        """
    )

    parser.add_argument("image_path", help="画像ファイルのパス")
    parser.add_argument("--url", "-u", help="画像のURL（指定すると直接検索URLを生成）")
    parser.add_argument("--upload", action="store_true", help="imgbbにアップロードしてURLを生成")
    parser.add_argument("--hash-only", action="store_true", help="ハッシュ値のみ表示")

    args = parser.parse_args()

    # ファイル存在確認
    if not os.path.exists(args.image_path):
        print(f"Error: ファイルが見つかりません: {args.image_path}", file=sys.stderr)
        sys.exit(1)

    print("## 逆画像検索\n")

    # 画像情報
    info = get_image_info(args.image_path)
    print("### 画像情報")
    print(f"- ファイル名: {info['filename']}")
    print(f"- サイズ: {info['size_bytes']:,} bytes")
    if 'width' in info:
        print(f"- 解像度: {info['width']} x {info['height']}")
        print(f"- フォーマット: {info.get('format', 'N/A')}")
    print()

    # ハッシュ値
    hashes = calculate_image_hashes(args.image_path)
    print("### ハッシュ値")
    print(f"- MD5: `{hashes['md5']}`")
    print(f"- SHA256: `{hashes['sha256']}`")
    print()

    if args.hash_only:
        return

    # 画像URL取得（指定またはアップロード）
    image_url = args.url

    if args.upload and not image_url:
        print("### 画像アップロード")
        image_url = upload_to_imgbb(args.image_path)
        if image_url:
            print(f"- アップロード成功: {image_url}")
        else:
            print("- アップロード失敗（IMGBB_API_KEY環境変数を設定してください）")
        print()

    # 検索URL生成
    urls = generate_search_urls(args.image_path, image_url)

    print("### 逆画像検索リンク")

    if image_url:
        print("\n**直接検索（URLベース）:**")
        print(f"- Google Lens: {urls.get('google_lens', 'N/A')}")
        print(f"- Google Images: {urls.get('google_images', 'N/A')}")
        print(f"- Yandex: {urls.get('yandex', 'N/A')}")
        print(f"- TinEye: {urls.get('tineye', 'N/A')}")
        print(f"- Bing: {urls.get('bing', 'N/A')}")

    print("\n**手動アップロード:**")
    print(f"- Google Images: {urls['google_images_upload']}")
    print(f"- Yandex: {urls['yandex_upload']}")
    print(f"- TinEye: {urls['tineye_upload']}")
    print(f"- Bing Visual Search: {urls['bing_upload']}")

    print("\n**特殊用途:**")
    print(f"- PimEyes: {urls['pimeyes']}")
    print(f"- FaceCheck: {urls['facecheck']}")
    print(f"- Search4Faces: {urls['search4faces']}")
    print(f"- KarmaDecay: {urls['karmadecay']}")

    print("\n### 検索のヒント")
    print("- **Yandex**: ロシア・東欧の画像に強い")
    print("- **TinEye**: 画像の初出・変更履歴を追跡")
    print("- **Google Lens**: 物体・場所の認識に優れる")
    print("- **顔検索**: PimEyes, FaceCheck（プライバシー考慮が必要）")


if __name__ == "__main__":
    main()

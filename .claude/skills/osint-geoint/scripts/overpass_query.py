#!/usr/bin/env python3
"""
Overpass Turbo クエリツール

座標周辺のOpenStreetMapデータを検索する。

使用例:
    # 座標周辺500m以内のレストランを検索
    python overpass_query.py --lat 35.6812 --lon 139.7671 --radius 500 --amenity restaurant

    # 特定エリアの空港を検索
    python overpass_query.py --area "Tokyo" --aeroway aerodrome

    # カスタムタグで検索
    python overpass_query.py --lat 35.6812 --lon 139.7671 --tag "shop=supermarket"

    # クエリのみ生成（実行しない）
    python overpass_query.py --lat 35.6812 --lon 139.7671 --amenity hospital --query-only
"""

import argparse
import json
import sys
import urllib.parse
from typing import Optional, List

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


OVERPASS_API_URL = "https://overpass-api.de/api/interpreter"
OVERPASS_TURBO_URL = "https://overpass-turbo.eu/"


# よく使うタグのプリセット
TAG_PRESETS = {
    # 交通
    'airport': 'aeroway=aerodrome',
    'runway': 'aeroway=runway',
    'station': 'railway=station',
    'bus_stop': 'highway=bus_stop',
    'parking': 'amenity=parking',
    'fuel': 'amenity=fuel',

    # 飲食
    'restaurant': 'amenity=restaurant',
    'cafe': 'amenity=cafe',
    'fast_food': 'amenity=fast_food',
    'bar': 'amenity=bar',

    # 宿泊
    'hotel': 'tourism=hotel',
    'hostel': 'tourism=hostel',

    # 公共施設
    'hospital': 'amenity=hospital',
    'school': 'amenity=school',
    'university': 'amenity=university',
    'library': 'amenity=library',
    'police': 'amenity=police',
    'fire_station': 'amenity=fire_station',

    # 商業
    'supermarket': 'shop=supermarket',
    'convenience': 'shop=convenience',
    'mall': 'shop=mall',
    'bank': 'amenity=bank',
    'atm': 'amenity=atm',

    # 観光
    'museum': 'tourism=museum',
    'monument': 'historic=monument',
    'viewpoint': 'tourism=viewpoint',
    'attraction': 'tourism=attraction',

    # 宗教
    'church': 'amenity=place_of_worship][religion=christian',
    'mosque': 'amenity=place_of_worship][religion=muslim',
    'temple': 'amenity=place_of_worship][religion=buddhist',
    'shrine': 'amenity=place_of_worship][religion=shinto',
}


def build_query(
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    radius: int = 500,
    area: Optional[str] = None,
    tags: List[str] = None,
    timeout: int = 25
) -> str:
    """Overpass QLクエリを構築"""

    query_parts = [f"[out:json][timeout:{timeout}];"]

    # エリア指定
    if area:
        query_parts.append(f'area["name"="{area}"]->.searchArea;')
        location_filter = "(area.searchArea)"
    elif lat is not None and lon is not None:
        location_filter = f"(around:{radius},{lat},{lon})"
    else:
        raise ValueError("座標 (lat/lon) またはエリア名が必要です")

    # タグごとのクエリを構築
    if not tags:
        tags = ['amenity=*']

    query_parts.append("(")
    for tag in tags:
        # 複合タグ（key=value形式）をパース
        if '=' in tag:
            key, value = tag.split('=', 1)
            tag_filter = f'["{key}"="{value}"]' if value != '*' else f'["{key}"]'
        else:
            tag_filter = f'["{tag}"]'

        query_parts.append(f'  node{tag_filter}{location_filter};')
        query_parts.append(f'  way{tag_filter}{location_filter};')
        query_parts.append(f'  relation{tag_filter}{location_filter};')

    query_parts.append(");")
    query_parts.append("out body;")
    query_parts.append(">;")
    query_parts.append("out skel qt;")

    return "\n".join(query_parts)


def execute_query(query: str) -> dict:
    """Overpass APIにクエリを実行"""
    if not REQUESTS_AVAILABLE:
        raise ImportError("requestsライブラリが必要です")

    response = requests.post(
        OVERPASS_API_URL,
        data={'data': query},
        timeout=60
    )

    response.raise_for_status()
    return response.json()


def format_results(data: dict) -> List[dict]:
    """API結果を整形"""
    results = []

    for element in data.get('elements', []):
        if element['type'] not in ['node', 'way', 'relation']:
            continue

        tags = element.get('tags', {})
        if not tags:
            continue

        result = {
            'type': element['type'],
            'id': element['id'],
            'name': tags.get('name', tags.get('name:en', tags.get('name:ja', 'N/A'))),
            'tags': tags
        }

        # 座標を取得
        if element['type'] == 'node':
            result['lat'] = element.get('lat')
            result['lon'] = element.get('lon')
        elif 'center' in element:
            result['lat'] = element['center'].get('lat')
            result['lon'] = element['center'].get('lon')

        results.append(result)

    return results


def generate_turbo_url(query: str) -> str:
    """Overpass Turbo用のURLを生成"""
    encoded = urllib.parse.quote(query)
    return f"{OVERPASS_TURBO_URL}?Q={encoded}"


def main():
    parser = argparse.ArgumentParser(
        description="Overpass Turbo クエリツール - OSMデータを検索",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
プリセットタグ:
{chr(10).join(f'  {k}: {v}' for k, v in sorted(TAG_PRESETS.items()))}

使用例:
  # 東京駅周辺500mのレストラン
  python overpass_query.py --lat 35.6812 --lon 139.7671 --preset restaurant

  # 成田空港の滑走路
  python overpass_query.py --area "Narita" --preset runway

  # カスタムタグで検索
  python overpass_query.py --lat 35.6812 --lon 139.7671 --tag "tourism=museum"

  # 複数タグを同時検索
  python overpass_query.py --lat 35.6812 --lon 139.7671 --tag "amenity=restaurant" --tag "amenity=cafe"
        """
    )

    # 位置指定
    parser.add_argument("--lat", type=float, help="緯度")
    parser.add_argument("--lon", type=float, help="経度")
    parser.add_argument("--radius", "-r", type=int, default=500, help="検索半径（メートル、デフォルト: 500）")
    parser.add_argument("--area", "-a", help="エリア名（例: Tokyo, New York）")

    # タグ指定
    parser.add_argument("--tag", "-t", action="append", dest="tags", help="検索タグ（key=value形式）")
    parser.add_argument("--preset", "-p", choices=TAG_PRESETS.keys(), help="プリセットタグを使用")

    # オプション
    parser.add_argument("--timeout", type=int, default=25, help="タイムアウト秒数（デフォルト: 25）")
    parser.add_argument("--query-only", "-q", action="store_true", help="クエリのみ生成（実行しない）")
    parser.add_argument("--json", action="store_true", help="結果をJSON形式で出力")
    parser.add_argument("--limit", "-l", type=int, default=20, help="表示件数上限（デフォルト: 20）")

    args = parser.parse_args()

    # 入力検証
    if not args.area and (args.lat is None or args.lon is None):
        parser.error("--lat と --lon、または --area が必要です")

    # タグの準備
    tags = args.tags or []
    if args.preset:
        tags.append(TAG_PRESETS[args.preset])
    if not tags:
        tags = ['amenity=*']

    # クエリ構築
    try:
        query = build_query(
            lat=args.lat,
            lon=args.lon,
            radius=args.radius,
            area=args.area,
            tags=tags,
            timeout=args.timeout
        )
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print("## Overpass Turbo クエリ\n")

    # クエリ表示
    print("### 検索条件")
    if args.lat is not None:
        print(f"- 座標: {args.lat}, {args.lon}")
        print(f"- 半径: {args.radius}m")
    if args.area:
        print(f"- エリア: {args.area}")
    print(f"- タグ: {', '.join(tags)}")
    print()

    print("### 生成されたクエリ")
    print("```overpass")
    print(query)
    print("```")
    print()

    # Overpass Turbo URL
    turbo_url = generate_turbo_url(query)
    print(f"### Overpass Turbo で開く")
    print(f"{turbo_url}")
    print()

    if args.query_only:
        return

    # クエリ実行
    if not REQUESTS_AVAILABLE:
        print("**注意**: requestsライブラリがインストールされていないため、クエリを実行できません。")
        print("上記のURLをブラウザで開くか、`pip install requests` を実行してください。")
        return

    print("### 検索結果")
    print("クエリを実行中...")

    try:
        data = execute_query(query)
        results = format_results(data)

        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
            return

        if not results:
            print("\n該当する結果がありませんでした。")
            return

        print(f"\n{len(results)}件の結果が見つかりました（上位{min(len(results), args.limit)}件を表示）:\n")

        print("| 名前 | タイプ | 座標 | 主要タグ |")
        print("|------|--------|------|----------|")

        for result in results[:args.limit]:
            name = result['name'][:30] if len(result['name']) > 30 else result['name']
            lat = result.get('lat', 'N/A')
            lon = result.get('lon', 'N/A')
            coord = f"{lat:.4f}, {lon:.4f}" if isinstance(lat, float) else "N/A"

            # 主要タグを抽出
            main_tags = []
            for key in ['amenity', 'shop', 'tourism', 'aeroway', 'railway', 'highway']:
                if key in result['tags']:
                    main_tags.append(f"{key}={result['tags'][key]}")
            tag_str = ", ".join(main_tags[:2]) if main_tags else "other"

            print(f"| {name} | {result['type']} | {coord} | {tag_str} |")

        if len(results) > args.limit:
            print(f"\n...他 {len(results) - args.limit} 件")

    except requests.exceptions.Timeout:
        print("\nError: タイムアウトしました。--timeout を増やすか、検索範囲を狭めてください。")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"\nError: API呼び出しに失敗しました: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

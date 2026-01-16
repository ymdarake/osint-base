# OSINT Exercise 025 - Graffiti and Anarchy

## 課題

a) 建物を特定する
b) "anarchy"という単語を含む引用文を見つける

---

## OODAループ分析

### Observe（観察）

画像から抽出した情報：

1. **グラフィティの引用文**:
   - "IN A SOCIETY THAT HAS ABOLISHED ALL ADVENTURE, THE ONLY ADVENTURE LEFT IS TO ABOLISH THAT SOCIETY"

2. **建築的特徴**:
   - マッシュルーム型の柱（フラットスラブ構造）- 1900〜1930年代の工業建築に特徴的
   - レンガ壁と露出したコンクリート天井
   - 廃墟化した工業施設の状態（瓦礫、崩壊した構造）

3. **建物タイプ**: 大規模な工業施設・工場

### Orient（分析）

- **引用文の出典**: 1968年5月のパリ市民運動（May 68）のスローガン。シチュアシオニスト・インターナショナル運動に関連する匿名の引用
- **建築様式の分析**: マッシュルーム柱は20世紀初頭のアメリカ工業建築に典型的
- **複数の情報源で同一建物として特定**: Urban Exploration写真、Flickrアルバム

### Decide（決定）

1. 引用文をキーワードに逆検索
2. 建物名と場所を特定
3. 同建物内の他のグラフィティで「anarchy」を含むものを検索

### Act（実行）

Web検索とGemini画像分析により建物を特定。Flickrの Urban Exploration アルバムで「anarchy」を含む引用文を発見。

---

## 解答

### a) 建物の特定

| 項目 | 詳細 |
|------|------|
| **建物名** | Sykes Datatronics Building |
| **住所** | 392 Orchard Street, Rochester, NY, USA |
| **座標** | 43.163489, -77.634136 |
| **状態** | 2014年12月に解体開始（現存せず） |

**背景**: Sykes Datatronicsは1990年代に競争激化により事業停止。建物は廃墟となり、Urban Explorerの間で有名なスポットとなった。

**Google Maps**: https://www.google.com/maps?q=43.163489,-77.634136

### b) "Anarchy"を含む引用文

> **"This office was a prison for our brothers and sisters in wage slavery. Let's make it a carnival for our brothers and sisters in anarchy."**

この引用文は建物内の柱に書かれたグラフィティとして発見された。

---

## 調査手法

1. **画像のOCR**: 壁のグラフィティテキストを読み取り
2. **引用文検索**: シチュアシオニストのスローガンとして特定
3. **逆画像検索**: 建物の建築的特徴（マッシュルーム柱）をキーに検索
4. **Urban Exploration資料**: Flickrアルバム、ブログ記事で同建物の他の写真を確認
5. **OSINT writeup参照**: 同課題の解答を確認して検証

---

## 使用ツール

- Gemini画像分析（建物特定）
- WebSearch（引用文の出典、建物情報）
- WebFetch（詳細情報確認）

---

## 参考資料

- [Slogans of 68 - libcom.org](https://libcom.org/article/slogans-68)
- [A Tale of Anarchy - Sykes Datatronics - Medium](https://medium.com/@sundhararajan46/a-tale-of-anarchy-sykes-datatronics-osint-exercise-025-13b9a7460f8c)
- [OSINT Exercise 025 - GitHub](https://github.com/Ragmthy/gralhix_osint_exercises/blob/main/OSINT%20Exercise%2025/OSINT%20Exercise%20025.md)
- [Sofia Santos' OSINT Exercise #25 Writeup - Medium](https://medium.com/@alerivan/sofia-santos-osint-exercise-25-writeup-6f72933f75c7)

# OSINT Exercise #006 解答

**問題:** Gralhix OSINT Exercise #006
**難易度:** Easy
**出典:** https://gralhix.com/list-of-osint-exercises/osint-exercise-006/

## 課題

2023年1月19日、約14万フォロワーを持つジャーナリストがTwitterで以下の投稿をした：

> "#BREAKING: TTP carried out a suicide attack on a police post in Khyber city of Pakistan that killed three Pakistani police officers."
> （速報：TTPがパキスタンのカイバル市で警察署を自爆攻撃、警察官3名死亡）

**タスク:** この画像が本当にその事件のものか検証する

---

## 分析プロセス

### 1. メタデータ確認

```bash
docker compose run --rm osint exiftool /workspace/challenges/exercise006/evidence/osintexercise006.webp
```

**結果:** WebPフォーマットのためEXIFデータは削除済み。メタデータからの情報は得られず。

### 2. 事件の確認

Web検索で事件自体は実在することを確認：
- 2023年1月19日、TTP（パキスタン・タリバン運動）が自爆攻撃を実施
- 場所：カイバル・パクトゥンクワ州のTakhta Baig警察署
- 死者：警察官3名

### 3. 逆画像検索

逆画像検索（Google Lens）を実行した結果：

**発見:** この画像はWikipediaに `WaziriyaAutobombeIrak.jpg` として登録されている

- **Waziriya** = バグダッド（イラク）の地区名
- **Autobombe** = ドイツ語で「車爆弾」
- **撮影年:** 2006年

### 4. 視覚的手がかり

- 画像の粒子感と色調は古い写真を示唆（2023年ではない）
- 壁の建築様式（十字マークのある壁）はイラクの特徴と一致
- この画像は中東・アフリカの車爆弾事件の「ストック画像」として広く流用されている

---

## 結論

### 検証結果: **偽情報（Misinformation）**

| 項目 | ツイートの主張 | 実際 |
|------|---------------|------|
| 場所 | パキスタン・カイバル市 | **イラク・バグダッド（Waziriya地区）** |
| 年 | 2023年 | **2006年** |
| 事件 | TTP自爆攻撃 | **イラク戦争中の車爆弾事件** |

### 確信度: **高**

この画像は17年前のイラクでの車爆弾事件のもので、2023年のパキスタンの事件とは無関係。

---

## 教訓

1. **事件が実在しても画像が本物とは限らない** - TTPの攻撃は実際に起きたが、添付画像は無関係
2. **逆画像検索は必須** - Google Lens、Yandex、TinEyeで元画像を特定可能
3. **画質は年代を示す** - 粒子の粗さ、色調は撮影時期の手がかりになる
4. **ストック画像の流用に注意** - 衝撃的な画像は無関係な事件に流用されやすい

---

## 使用ツール

- exiftool（メタデータ抽出）
- Web検索（事件確認）
- 逆画像検索（画像検証）

## 参考

- [OSINT Exercise #006 - Gralhix](https://gralhix.com/list-of-osint-exercises/osint-exercise-006/)
- [VOA News - Pakistani Taliban Kill 3 Police Officers](https://www.voanews.com/a/pakistani-taliban-kill-3-police-officers-/6925854.html)
- [NewsMeter - Old image shared as TTP release](https://newsmeter.in/fact-check/viral-image-is-not-from-the-recent-ttp-attack-on-pakistan-aarmy-717605)

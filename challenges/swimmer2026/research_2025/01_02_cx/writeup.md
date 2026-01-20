# SWIMMER CTF 2026 - 啓徳空港100周年記念フライト

## 問題1: フライト便名

> 2025年春、かつて香港に存在していた空港の100周年を記念して、特別なフライトが実施されたようです。
> このフライトの便名を解答してください。

### Flag

```
SWIMMER{CX8100}
```

### 解法

- 「かつて香港に存在していた空港」→ 啓徳空港（Kai Tak Airport）
- 1925年開港 → 2025年が100周年
- 2025年3月30日、キャセイパシフィック航空が記念フライト **CX8100** を運航

---

## 問題2: パイロット特定

> CX の問題で示されたフライト中、添付画像の席に座っていた人物の名前を英語で解答してください。
> （添付画像はコックピット右席を指す矢印）

### Flag

```
SWIMMER{Adrian Scott}
```

### 解法

**Observe（観察）**
- 添付画像: コックピット、黄色矢印が**右席（First Officer / 副操縦士席）**を指している
- CX8100便の右席パイロットを特定する必要がある

**Orient（分析）**

CX8100便のクルー情報:

| パイロット | 役職 | 推定座席 |
|-----------|------|----------|
| Geoffrey Lui | Chief Pilot (Airbus) | 左席（Captain/PIC） |
| Adrian Scott | Flying Training Manager | 右席（First Officer） |

**Decide（決定）**

座席配置の根拠:
1. 「Commanded by Chief Airbus Test Pilot Geoffrey Lui and CX's Flying Training Manager Adrian Scott」の表現で、Chief Pilotが先に言及（通常はPICが先）
2. 航空業界の慣例として、Fleet Chief（最高位）は左席（Captain席）に座る
3. Geoffrey Lui は Chief Pilot（最上位役職）であり、PICとして左席が妥当
4. Adrian Scott は Flying Training Manager で、右席（First Officer席）

**Act（実行）**

右席 = **Adrian Scott**

---

## 参考資料

- [Geoffrey Lui '95 - CIS Alumni Connect](https://cisalumniconnect.org/geoffrey-lui-95-aviation-cathay-pacific-and-kai-tak-tribute-flight-cx8100/)
- [Cathay Pacific returns to Kai Tak - Checkerboard Hill](https://www.checkerboardhill.com/2025/04/cathay-pacific-flyby-kai-tak-flight-cx8100/)
- [Campaign Brief Asia - CX8100](https://campaignbriefasia.com/2025/04/11/flight-cx8100-takes-off-cathay-soars-once-more-over-kai-tak-in-tribute-to-legendary-flight-path/)
- [CX8100 special flight - FlyerTalk](https://www.flyertalk.com/forum/cathay-pacific-cathay/2190677-cx8100-special-flight-march-30th-4pm-over-kai-tak.html)

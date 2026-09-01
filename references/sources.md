# 一次情報の場所

> 🔴 **AI の記憶で答えない。ここに当たらせる。**
> 🔴 **リンクは切れる。毎回アクセスして生存を確かめる。**

## 検算のさせ方（プロンプトの型）

```
【調べること】○○
【条件】
- 根拠は次のドメインの情報だけを使う: nta.go.jp / moj.go.jp / e-gov.go.jp
- 参照したURLを必ず出す
- 制度変更があった場合は「いつから」も書く
- 似た名前の役所・書類がある場合は、なぜそちらではないのかも書く
```

**最後の2行が効く。**
「いつから」を聞くと古い情報を根拠にしたときに破綻が出る。
「なぜそちらではないか」を聞くと、似た名前で間違えるパターンを潰せる。

## 国税（税務署）

| 何 | URL |
|---|---|
| **税務署の所在地・管轄一覧** | https://www.nta.go.jp/about/organization/access/map.htm |
| 法人設立届出書（様式・記載要領） | https://www.nta.go.jp/taxes/tetsuzuki/shinsei/annai/hojin/annai/1554_2.htm |
| **青色申告書の承認の申請（法人・C1-19）** | https://www.nta.go.jp/taxes/tetsuzuki/shinsei/annai/hojin/annai/1554_14.htm |
| **添付書類の簡素化**（登記事項証明書が不要になった根拠） | https://www.nta.go.jp/information/other/data/h29/kansoka/index.htm |
| 申告・申請・届出等の様式一覧（入口） | https://www.nta.go.jp/taxes/tetsuzuki/shinsei/index.htm |
| e-Tax | https://www.e-tax.nta.go.jp/ |

🔴 **管轄は「税務署の所在地・管轄一覧」で必ず確定する。**
都道府県名・市名から推測しない。同じ市の中でも区で分かれる。

## 設立手続の全体像（法務省）

| 何 | URL |
|---|---|
| **合同会社の設立手続について** | https://www.moj.go.jp/MINJI/minji06_00141.html |
| 株式会社の設立手続（発起設立）について | https://www.moj.go.jp/MINJI/minji06_00134.html |
| 登録免許税の税額表（国税庁 No.7191） | https://www.nta.go.jp/taxes/shiraberu/taxanswer/inshi/7191.htm |

このページで確認できる要点（2026-09 時点で原文を確認済み）:

- 🔴 **合同会社の定款は、公証人の認証を受ける必要がない**（株式会社は必要）
- **登録免許税は資本金の額 × 1000分の7。6万円に満たないときは1件につき6万円**
  （株式会社は同じ税率で**最低15万円**。登録免許税法別表第一 24号(一)）

## 登記（法務局）

| 何 | URL |
|---|---|
| 商業・法人登記の申請書様式 | https://houmukyoku.moj.go.jp/homu/COMMERCE_11-1.html |
| 法務局の管轄一覧 | https://houmukyoku.moj.go.jp/homu/static/kankatsu_index.html |
| 登記・供託オンライン申請システム | https://www.touki-kyoutaku-online.moj.go.jp/ |
| 登記事項証明書の交付請求 | https://houmukyoku.moj.go.jp/homu/static/online_syoumei_annai.html |

## 法人番号

| 何 | URL |
|---|---|
| **国税庁 法人番号公表サイト** | https://www.houjin-bangou.nta.go.jp/ |

登記完了後に法人番号が指定され、ここに自動で掲載される。
🔴 **ここに載っている表記が、登記の写し**。表記統一の基準として使える。

## 地方税

| 何 | URL |
|---|---|
| eLTAX（地方税ポータル） | https://www.eltax.lta.go.jp/ |
| 都道府県税事務所 | **各都道府県のサイト**（「○○県 法人設立 届出 様式」で探す） |
| 市区町村 | **各市区町村のサイト**（「○○市 法人設立・開設届出書」で探す） |

🔴 **東京23区は都税事務所に一本化**され、区への届出が不要。
→ https://www.tax.metro.tokyo.lg.jp/

## 法令

| 何 | URL |
|---|---|
| e-Gov 法令検索 | https://laws.e-gov.go.jp/ |
| 法人税法（設立届＝148条／青色＝122条） | e-Gov で「法人税法」を検索 |
| 会社法（合同会社＝第3編） | 同上 |

## 社会保険

| 何 | URL |
|---|---|
| 日本年金機構 適用事業所に関すること | https://www.nenkin.go.jp/service/kounen/tekiyo/jigyosho/index.html |

🔴 **役員報酬0なら被保険者にならない**ため、当面は不要になるケースがある。
報酬を出す段階で必ず再確認する。

## D-U-N-S® Number（Apple / Google の組織登録に要る）

| 何 | URL |
|---|---|
| Apple 向け D-U-N-S 番号の確認・申請 | https://developer.apple.com/enroll/duns-lookup/ |
| D&B（日本）東京商工リサーチ | https://www.tsr-net.co.jp/ |

- **無料ルートと有料ルートがある**。無料は発番までに時間がかかる
- 一度取れば **Apple / Google Play の両方で使い回せる**
- 🔴 **Apple は D&B の登録住所を自動入力する**（→ `notation.md`）

## 定款

| 何 | 備考 |
|---|---|
| 電子定款 | **印紙代4万円が不要**になる。ただし電子署名の環境が要る |
| 行政書士に依頼 | 数千円〜1万円台で電子定款だけ作ってもらえることが多い。**自分で環境を作るより安いことが多い** |
| 公証人役場 | **合同会社は定款認証が不要**（株式会社は必要） |

🔴 **合同会社は定款認証が不要**なので、株式会社より手順が2つ少なく、費用も安い。
（登録免許税も株式会社15万円〜に対し**合同会社6万円〜**）

## 使ってはいけない情報源

| ❌ | 理由 |
|---|---|
| 個人ブログ・まとめ記事の「必要書類一覧」 | **制度変更前のまま放置**されていることがある |
| AI の記憶だけの回答 | 学習時点で古い。管轄・様式・期限は特に危険 |
| 数年前の書籍 | 添付書類の簡素化など、直近の変更が反映されていない |

**判断に使ってよいのは官公庁のドメインだけ。**
まとめ記事は「何を調べるべきか」を知るためには使ってよいが、**根拠にはしない**。

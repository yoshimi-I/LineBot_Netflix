# Lineで行う,動画検索bot
## タイトル
- 動画紹介bot
## 概要
- 条件に一致したおすすめの動画を推薦してくれるやつ
  - リンクを踏めばそのままアプリが起動します
## アカウント(ここから追加してください)
- ![画像](https://user-images.githubusercontent.com/89241539/202895679-18c242de-7de5-4b1e-a54c-ea9f2ca007ab.png)
## 動機
- デザインセンスが皆無のため,ReactやVueは使いたくなかった
- ネトフリのおすすめが割としょぼいので一期一会という言葉を信じてランダムでおすすめしてくれる物が欲しかった
- ユーザーの評価を参考に改良を行いたかったため,みんなにたくさん触って欲しかった
  - その結果Linebotに行き着いた
## 使い方
- ユーザーはそれぞれ出される質問に答えていくと、自然とおすすめの映画,動画に行き着くようになっております
## 質問一覧
1. 動画の視聴方法
   1. ネットフリックス
   2. アマゾンプライム
   3. hulu
   4. ディズニープラス
   5. U-NEXT
2. 作品の種類
   1. 映画
   2. アニメ,ドラマ
3. 映画のジャンル
   1. アクション
   2. アニメーション
   3. コメディ
   4. 犯罪,戦争
   5. ドキュメンタリー
   6. SF
   7. ファンタジー
   8. 歴史
   9. ホラー,ミステリー
   10. ファミリー
   11. ミュージカル
   12. ロマンス
   13. スポーツ
4. 作品の評価
   1. top3
   2. top10 
   3. top100
   4. なんでもいい
5. 作品の公開日時
   1. ~2000
   2. 2000~2010
   3. 2010~2020
   4. 2020~現在

## デモ動画
### ver1.0
https://user-images.githubusercontent.com/89241539/202896092-c15d7043-9001-4de9-8f76-16f55e8409fa.mp4

### ver4.0
https://user-images.githubusercontent.com/89241539/203808209-f305903e-13e6-42a3-aafc-f385209c6c78.mp4


## アップデート履歴
- ver1.0 
  - リリース  
- ver2.0
  - ランキングによる評価の実装(top3,top,10)
- ver3.0
  - 評価による絞り込みの削除(top3,top10,top100,なんでもいいの中から選択を行う)
  - 公開日による映画の絞り込みの追加
- ver4.0
  - カードを3枚から5枚へ変更
  - 条件を変えずに再検索を行えるボタンを実装

   

# convert-togo-data
横浜市経済局のテイクアウト＆デリバリー情報オープンデータ（CSV）のクレンジング

横浜市経済局が収集している市内テイクアウト＆デリバリー情報を　YOKOHAMA to Goに取り込むためのクレンジング。

データはここから入手可能。
https://www.city.yokohama.lg.jp/business/kigyoshien/syogyo/covid-19/takeout-delivery/takeout.html

解決の必要があった課題
主に、「修正依頼」レコードに起因する問題。

- 修正依頼であることはわかるが、どのレコードに対する修正依頼か機械判別するのがかなり困難。
- 名称や電話番号表記まで変更になっているケースがある
- 複数回修正依頼が来ているケースがある
- おそらく、新規登録なのに修正依頼になっているエントリーがある

Pythonで書いたが、JSで書き直せしてYOKOHAMA to Goのレポジトリに持ち込むのが良いか。

HPBPwdBreaker
====

## 動作原理
詳しくは下に書いたサイト( http://www.usamimi.info/~geko/arch_web/03_memo/011_hpb/index.html )に書いてあるが、
HPビルダーのパスワード付きリンクを生成する機能で使われる暗号の脆弱性を利用して、
*リンクURLの最後が.htmlで終わると仮定して*可能性のあるパスワードとその時の復号化されたURLを列挙するプログラム。

## ファイルの説明
* chkpass.js --- パスワードチェック処理の部分を抜き出してちょっといじったもの
* hack.py --- メインのプログラム
* main.c --- Cに移植しようかと奮闘中のもの

## 参考にさせていただいたページ

*http://www.usamimi.info/~geko/arch_web/03_memo/011_hpb/index.html 
そもそもの暗号化方式の脆弱性について書いてあったところ
*http://hpbuilder.net/caution/password_link.html 
パスワード付きリンクのサンプルとしてテストに使用

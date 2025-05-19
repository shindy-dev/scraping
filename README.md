# scraping
icoon-monoのアイコンを全てダウンロードするプログラム。
保存場所、カテゴリ、拡張子、画像の解像度、色(rgb)の指定はmain.pyで行う必要がある

## 導入
- python3系以上必須
linux系OS や mac OS ではシステムでpythonの2系と3系が使われており、
python3系を使用する際のコマンドが「python3」となっているが本稿では「python」に
統一する。

```
python -m venv venv

# mac os or linux
source venv/bin/activate
# windows
venv\Scripts\activate

python -m pip selenium
```

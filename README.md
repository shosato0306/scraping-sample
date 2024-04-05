# scraping-sample

## requirement

以下のツールを事前にローカル PC にインストールしておく

- pyenv
  - python のバージョンマネージャツール
- poetry
  - python のパッケージマネージャツール

インストールについてはこの辺りが参考になるかも  
https://qiita.com/Ryku/items/512a6744bfa9903bf2dd

## set up

```bash
# 3.11.2 のバージョンをインストール
$ pyenv install 3.11.2
# python 3.11.2 環境に切り替え
$ pyenv local 3.11.2

# 必要なライブラリのインストール
$ poetry install --no-root
```

## run

```bash
$ poetry run python main.py main
```

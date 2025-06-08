# 論文要約ツール

このプロジェクトは、Google Gemini API を使用してPDF形式の論文を要約するツールです。要約されたテキストはMarkdown形式で保存されます。

-----

## 特徴

  * Google Gemini API を利用したPDF論文の自動要約
  * 要約結果をMarkdown形式で保存
  * 出力ファイル名はUUID5に基づいて一意に生成されるため、同じ論文からは常に同じファイル名が出力
  * 設定の柔軟性（モデルの選択、温度設定など）

-----

## セットアップ

### APIキーの取得

このツールを使用するには、Google Gemini API のAPIキーが必要です。以下の手順で取得してください。

1.  [Google AI Studio](https://aistudio.google.com/app/apikey) にアクセスします。
2.  Googleアカウントでログインします。
3.  「APIキーを作成」ボタンをクリックし、新しいAPIキーを生成します。
4.  生成されたAPIキーを控えておいてください。

### プロジェクトのクローン

まず、このリポジトリをあなたのローカル環境にクローンします。

```bash
git clone https://github.com/kawata-yuya/SummarizePapers.git
cd SummarizePapers
```

### Python環境のセットアップ

必要なPythonライブラリをインストールするために、仮想環境の利用を強く推奨します。

1.  **仮想環境の作成とアクティベート:**

    ```bash
    python -m venv vertex
    # Windowsの場合
    .\vertex\Scripts\activ
    # macOS/Linuxの場合
    source vertex/bin/activate
    ```

2.  **必要なライブラリのインストール:**
    プロジェクトのルートディレクトリにある`requirements.txt`ファイルから、必要なライブラリをインストールします。

    ```bash
    pip install -r requirements.txt
    ```


### APIキーファイルの設定

取得したAPIキーは、プロジェクトのルートディレクトリに `gemini_api_key.json` という名前で保存する必要があります。このファイルはGitによって無視されるよう設定されており、あなたのAPIキーが誤って公開されることを防ぎます。

1.  プロジェクトのルートディレクトリに `gemini_api_key.json` ファイルを作成します。

2.  以下の形式で、取得したAPIキーを記述します。

    ```json
    {
        "key": "YOUR_YOUR_GEMINI_API_KEY_HERE"
    }
    ```

    `YOUR_YOUR_GEMINI_API_KEY_HERE` の部分を、あなたの実際のAPIキーに置き換えてください。

-----

## 使い方

要約したいPDFファイルを `papers/` ディレクトリに配置し、以下のスクリプトを実行します。

```bash
python your_main_script_name.py # 例: python summarize.py
```

`your_main_script_name.py` は、`PaperSummarizer` クラスをインスタンス化して `summarize_paper` メソッドを呼び出すスクリプトです（例として提供した `if __name__ == "__main__":` ブロックのようなコードが含まれるファイル）。

要約されたテキストは `output/` ディレクトリに、PDFファイルパスに基づいて生成されたUUID5をファイル名とするMarkdownファイルとして保存されます。

-----

## ファイル構成

プロジェクトの主なファイル構成は以下の通りです。

```
.
├── papers/
│   └── data.pdf             # 要約したいPDF論文を配置するディレクトリ
├── output/
│   └── (要約されたMarkdownファイル) # 生成された要約が保存されるディレクトリ
├── gemini_api_key.json      # APIキーを保存するファイル（.gitignoreで管理）
├── prompt.txt               # Gemini APIへのプロンプトテキスト
├── requirements.txt         # 必要なPythonライブラリのリスト
├── your_main_script_name.py # メインのPythonスクリプト (例: summarize.py)
└── README.md                # このREADMEファイル
```


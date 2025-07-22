# Morpholyzer - 日本語形態素解析アプリ

DjangoとMeCabを使用した日本語形態素解析Webアプリケーションです。

## 概要

Morpholyzerは、日本語テキストを入力すると、MeCabを使用して形態素解析を行い、各単語の品詞、原形、読み方などの詳細情報を表形式で表示するWebアプリケーションです。

## 主な機能

- 🔤 **日本語形態素解析**: MeCabを使用した高精度な形態素解析
- 📊 **結果の視覚化**: 解析結果を見やすい表形式で表示
- 📈 **品詞統計**: 入力テキストの品詞分布を表示
- 🌐 **レスポンシブデザイン**: Bootstrap を使用したモバイル対応UI
- 🔌 **API対応**: JSON形式でデータを取得可能なAPIエンドポイント
- 🐳 **Docker対応**: 簡単なデプロイメントとポータビリティ

## 技術スタック

- **Backend**: Django 5.2.4
- **形態素解析**: MeCab + mecab-ipadic-utf8
- **Frontend**: HTML5, Bootstrap 5.1.3
- **データベース**: SQLite3 (デフォルト)
- **コンテナ**: Docker & Docker Compose

## システム要件

### ローカル環境
- Python 3.12以上
- MeCab
- mecab-ipadic-utf8 辞書

### Docker環境
- Docker
- Docker Compose

## セットアップ方法

### 方法1: ローカル環境でのセットアップ

#### 1. リポジトリのクローン
```bash
git clone https://github.com/TakuyaFukumura/morpholyzer.git
cd morpholyzer
```

#### 2. MeCabのインストール

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install mecab mecab-ipadic-utf8
```

**macOS (Homebrew):**
```bash
brew install mecab mecab-ipadic
```

**Windows:**
[MeCab公式サイト](https://taku910.github.io/mecab/)からダウンロードしてインストール

#### 3. Python仮想環境の作成と有効化
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

#### 4. 依存関係のインストール
```bash
pip install -r requirements.txt
```

#### 5. データベースのマイグレーション
```bash
python manage.py migrate
```

#### 6. アプリケーションの起動
```bash
python manage.py runserver
```

ブラウザで `http://localhost:8000` にアクセスしてください。

### 方法2: Dockerでのセットアップ

#### 1. リポジトリのクローン
```bash
git clone https://github.com/TakuyaFukumura/morpholyzer.git
cd morpholyzer
```

#### 2. Dockerコンテナの起動
```bash
# 本番用
docker-compose up web

# 開発用（ボリュームマウント付き）
docker-compose up dev
```

ブラウザで `http://localhost:8000` にアクセスしてください。

## 使い方

### Webインターフェース

1. ブラウザで `http://localhost:8000` にアクセス
2. テキスト入力欄に日本語テキストを入力
3. 「解析実行」ボタンをクリック
4. 解析結果が表形式で表示されます

### API使用例

```bash
# POSTリクエストで形態素解析を実行
curl -X POST http://localhost:8000/api/analyze/ \
  -d "text=これは日本語のテストです。"

# レスポンス例
{
  "success": true,
  "original_text": "これは日本語のテストです。",
  "morphemes": [
    {
      "surface": "これ",
      "pos": "名詞",
      "pos_detail1": "代名詞",
      "pos_detail2": "一般",
      "base_form": "これ",
      "reading": "コレ",
      "pronunciation": "コレ"
    }
    // ... 他の形態素
  ],
  "pos_summary": {
    "名詞": 2,
    "助詞": 2,
    "助動詞": 1,
    "記号": 1
  },
  "total_morphemes": 7
}
```

## 開発

### テストの実行
```bash
# 全テストの実行
python manage.py test

# 特定のアプリのテスト
python manage.py test morpholyzer

# カバレッジ付きテスト実行
pip install coverage
coverage run --source='.' manage.py test morpholyzer
coverage report
```

### 開発サーバーの起動
```bash
python manage.py runserver
```

### Docker開発環境
```bash
# 開発用コンテナの起動（ファイル変更が自動反映）
docker-compose up dev

# コンテナ内でのシェル実行
docker-compose exec dev bash

# テストの実行
docker-compose exec dev python manage.py test
```

## プロジェクト構造

```
morpholyzer/
├── morpholyzer_project/    # Djangoプロジェクト設定
│   ├── settings.py         # Django設定
│   ├── urls.py            # URLルーティング
│   └── ...
├── morpholyzer/           # メインアプリケーション
│   ├── analyzer.py        # 形態素解析ロジック
│   ├── forms.py          # Djangoフォーム
│   ├── views.py          # ビューロジック
│   ├── urls.py           # アプリURL設定
│   ├── tests.py          # テストケース
│   └── templates/        # HTMLテンプレート
├── requirements.txt       # Python依存関係
├── Dockerfile            # Dockerイメージ定義
├── docker-compose.yml    # Docker Compose設定
├── .dockerignore         # Docker除外ファイル
└── README.md             # このファイル
```

## API仕様

### POST /api/analyze/

形態素解析を実行するAPIエンドポイント

**リクエスト:**
- Method: POST
- Content-Type: application/x-www-form-urlencoded
- Parameters:
  - `text`: 解析対象の日本語テキスト (必須, 最大1000文字)

**レスポンス:**
```json
{
  "success": true,
  "original_text": "入力テキスト",
  "morphemes": [
    {
      "surface": "表層形",
      "pos": "品詞",
      "pos_detail1": "品詞細分類1",
      "pos_detail2": "品詞細分類2", 
      "pos_detail3": "品詞細分類3",
      "inflection_type": "活用型",
      "inflection_form": "活用形",
      "base_form": "原形",
      "reading": "読み",
      "pronunciation": "発音"
    }
  ],
  "pos_summary": {
    "品詞名": 出現回数
  },
  "total_morphemes": 形態素総数
}
```

## トラブルシューティング

### MeCabエラー
```
RuntimeError: 
Failed initializing MeCab.
```

**解決方法:**
1. MeCabがインストールされているか確認
2. 辞書が正しく配置されているか確認
3. 環境変数の設定を確認

### Dockerビルドエラー
```
ERROR: Could not find a version that satisfies the requirement Django==5.2.4
```

**解決方法:**
ネットワーク接続を確認し、Dockerfileの`--trusted-host`オプションを確認してください。

### ポートエラー
```
django.core.exceptions.DisallowedHost: Invalid HTTP_HOST header
```

**解決方法:**
`settings.py`の`ALLOWED_HOSTS`設定を確認してください。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 貢献

プルリクエストやIssueは歓迎です。以下の手順で開発に参加できます：

1. フォークする
2. フィーチャーブランチを作成する (`git checkout -b feature/amazing-feature`)
3. 変更をコミットする (`git commit -m 'Add some amazing feature'`)
4. ブランチをプッシュする (`git push origin feature/amazing-feature`)
5. プルリクエストを作成する

## 作者

[TakuyaFukumura](https://github.com/TakuyaFukumura)

## 参考資料

- [Django公式ドキュメント](https://docs.djangoproject.com/)
- [MeCab公式サイト](https://taku910.github.io/mecab/)
- [Bootstrap公式ドキュメント](https://getbootstrap.com/docs/)

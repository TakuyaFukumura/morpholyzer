# Morpholyzer - 日本語形態素解析アプリケーション

MorpholyzerはMeCabを使用した日本語形態素解析のためのDjangoウェブアプリケーションです。Webインターフェースと REST APIの両方を提供し、日本語テキストを詳細な言語情報を含む形態素に解析します。

**必ずこれらの指示を最初に参照し、ここにある情報と一致しない予期しない情報に遭遇した場合のみ、検索やbashコマンドにフォールバックしてください。**

## 効果的な作業方法

### 前提条件と環境設定
- MeCabはmecab-ipadic-utf8辞書とともにシステム全体にインストール済み
- Python 3.12が`/usr/bin/python3`で利用可能
- DockerとDocker Compose（v2構文）が利用可能

### リポジトリのブートストラップとビルド
**ビルドや長時間実行されるコマンドを絶対にキャンセルしないでください。完了まで待機してください。**

```bash
# 1. Python依存関係のインストール - 約6秒
pip install -r requirements.txt

# 2. データベースマイグレーションの実行 - 約0.5秒  
python manage.py migrate

# 3. 全テストの実行 - 約1秒。絶対にキャンセルしないでください。
python manage.py test
# 期待される結果: "Ran 13 tests in 0.XXXs OK"

# 4. 特定のアプリテストの実行 - 約0.5秒
python manage.py test morpholyzer
```

### アプリケーションの実行

#### ローカル開発サーバー
```bash
# 開発サーバーの開始 - 約2秒で起動
python manage.py runserver
# アクセス先: http://localhost:8000
# APIエンドポイント: http://localhost:8000/api/analyze/
```

#### Docker環境
```bash
# Dockerイメージのビルド - 約23秒。絶対にキャンセルしないでください。タイムアウトを60秒以上に設定してください。
docker compose build web

# 本番コンテナの実行 - 約5秒で起動
docker compose up web
# アクセス先: http://localhost:8000

# 開発コンテナの実行（ボリュームマウント付き）
docker compose up dev
# 注意: 一部の環境ではコンテナランタイムの問題により失敗する可能性があります
```

### テストと品質保証

#### テストコマンド
```bash
# 時間測定付きで全テストを実行
time python manage.py test
# 期待される時間: 約1秒。絶対にキャンセルしないでください。

# カバレッジ分析付きで実行
pip install coverage
coverage run --source='.' manage.py test morpholyzer
coverage report
# 期待される結果: 約90%のカバレッジ、約1秒で実行
```

#### APIテスト
```bash
# 日本語サンプルテキストでAPIエンドポイントをテスト
curl -X POST -d "text=これはテストです。" http://localhost:8000/api/analyze/
# 期待される結果: morphemes配列とpos_summaryを含むJSONレスポンス
```

## 検証シナリオ

**変更を行った後は、必ずこれらの検証シナリオを実行してください:**

### 1. 基本機能テスト
1. 開発サーバーを開始: `python manage.py runserver`
2. http://localhost:8000 に移動
3. 日本語テキストを入力: `これは日本語形態素解析のテストです。`
4. 送信ボタンをクリック
5. 解析結果が表示されることを確認:
   - 品詞統計 (POS statistics)
   - 解析情報 (Analysis information)
   - 完全な形態素分解テーブル

### 2. API検証テスト  
```bash
# 有効な入力をテスト
curl -X POST -d "text=テスト文章" http://localhost:8000/api/analyze/

# 空の入力をテスト（400エラーが返されるべき）
curl -X POST -d "text=" http://localhost:8000/api/analyze/

# 無効なメソッドをテスト（405エラーが返されるべき）
curl -X GET http://localhost:8000/api/analyze/
```

### 3. テストスイート検証
```bash
# 全テストが通過する必要があります
python manage.py test
# 期待される出力: "Ran 13 tests in X.XXXs OK"
```

## よく使用するタスクとファイルの場所

### 主要なアプリケーションコンポーネント
- **メインアプリ**: `morpholyzer/` - 形態素解析のコアロジック
- **MeCab統合**: `morpholyzer/analyzer.py` - MorphologicalAnalyzerクラス
- **Webビュー**: `morpholyzer/views.py` - WebとAPIのDjangoビュー
- **テンプレート**: `morpholyzer/templates/morpholyzer/index.html` - Webインターフェース
- **テスト**: `morpholyzer/tests.py` - 13の包括的なテストケース
- **フォーム**: `morpholyzer/forms.py` - テキスト入力検証
- **設定**: `morpholyzer_project/settings.py` - Django設定

### プロジェクト構造リファレンス
```
├── manage.py                 # Django管理スクリプト
├── requirements.txt          # Python依存関係 (Django 5.2.4, mecab-python3)
├── Dockerfile               # コンテナ定義
├── docker-compose.yml       # Dockerサービス (web, dev)
├── morpholyzer/            # メインDjangoアプリ
│   ├── analyzer.py         # MeCab形態素解析
│   ├── views.py           # WebとAPIエンドポイント  
│   ├── tests.py           # テストスイート (13テスト)
│   ├── forms.py           # 入力検証
│   └── templates/         # HTMLテンプレート
└── morpholyzer_project/   # Djangoプロジェクト設定
    ├── settings.py        # 設定
    └── urls.py           # URLルーティング
```

### データベース情報
- **エンジン**: SQLite3（開発デフォルト）
- **場所**: `db.sqlite3`（自動作成）
- **マイグレーション**: 標準のDjango認証とセッションテーブルのみ
- **カスタムモデルなし**: アプリケーションは形態素解析においてステートレス

### API仕様
- **エンドポイント**: `POST /api/analyze/`
- **入力**: `text`パラメータ（最大1000文字）
- **出力**: morphemes配列、pos_summary、メタデータを含むJSON
- **エラーコード**: 400（空のテキスト）、405（間違ったメソッド）、500（解析エラー）

## 実行時間の期待値とタイムアウト

**重要: これらの操作を絶対にキャンセルしないでください:**

- **依存関係のインストール**: 約6秒（タイムアウト設定: 60秒以上）
- **データベースマイグレーション**: 約0.5秒（タイムアウト設定: 30秒以上） 
- **テスト実行**: 約1秒（タイムアウト設定: 30秒以上）
- **Dockerビルド**: 約23秒（タイムアウト設定: 60秒以上）
- **サーバー起動**: 約2秒（タイムアウト設定: 30秒以上）
- **カバレッジ分析**: 約1秒（タイムアウト設定: 30秒以上）

## トラブルシューティング

### MeCabの問題
MeCab初期化エラーが発生した場合:
1. MeCabのインストールを確認: `mecab --version`
2. 辞書を確認: `ls /usr/share/mecab/dic/`
3. MeCabはシステム全体にプリインストール済み - 再インストールしないでください

### Dockerの問題  
- `docker compose`（v2構文）を使用し、`docker-compose`は使用しないでください
- 開発コンテナはランタイムの問題により失敗する可能性があります - 代わりに本番コンテナを使用してください
- docker-compose.ymlの古いversion属性に関する警告は無害です

### ポート競合
- デフォルトポート8000が使用中の可能性があります
- 代替ポートを使用: `python manage.py runserver 127.0.0.1:8001`

### テスト失敗
- 13のテストすべてが一貫して通過する必要があります
- テストが失敗する場合は、MeCabのインストールと日本語テキストエンコーディングを確認してください
- テストデータベースは自動的に作成/削除されます

## 開発ノート

### コードスタイルと標準
- アプリケーションはUIテキストとコメントに日本語を使用します
- 既存のDjangoパターンと規約に従ってください  
- MeCabアナライザーはUTF-8日本語テキストエンコーディングを自動的に処理します
- エラーメッセージはUI言語に合わせて日本語で表示されます

### 変更を行う場合
- 修正後は必ず完全なテストスイートを実行: `python manage.py test`
- WebインターフェースとAPIエンドポイントの両方を手動でテストしてください
- MeCab解析が日本語サンプルテキストで正常に動作することを確認してください
- 形態素解析が期待される言語的特徴を返すことを確認してください

### 依存関係
- **Django 5.2.4**: Webフレームワーク
- **mecab-python3 1.0.10**: 形態素解析のためのMeCabバインディング
- **リンティングツールなし**: プロジェクトにはESLint、Flake8などは含まれていません
- **CI/CDなし**: GitHub Actionsワークフローは設定されていません

### 動作確認済みコマンド一覧
```bash
# 完全な検証シーケンス（すべてのコマンドを実行）:
pip install -r requirements.txt              # 約6秒
python manage.py migrate                     # 約0.5秒  
python manage.py test                        # 約1秒
python manage.py runserver                   # 約2秒で起動
curl -X POST -d "text=テスト" http://localhost:8000/api/analyze/  # APIテスト
docker compose build web                     # 約23秒
docker compose up web                        # 約5秒で起動
```
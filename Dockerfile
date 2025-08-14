# Pythonベースイメージを使用
FROM python:3.12-slim

# 環境変数の設定
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# システムパッケージの更新とMeCabのインストール
RUN apt-get update && apt-get install -y \
    mecab \
    mecab-ipadic-utf8 \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリの設定
WORKDIR /app

# 依存関係ファイルをコピー
COPY requirements.txt .

# Python依存関係のインストール
RUN pip install --trusted-host pypi.org \
    --trusted-host pypi.python.org \
    --trusted-host files.pythonhosted.org \
    --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY . .

# 静的ファイルの収集とデータベースマイグレーション
RUN python manage.py collectstatic --noinput || echo "No static files to collect"
RUN python manage.py migrate

# ポート8000を公開
EXPOSE 8000

# アプリケーション実行
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

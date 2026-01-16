# OSINT CTF Workbench
# SWIMMER OSINT CTF 2026 用作業環境

FROM python:3.11-slim-bookworm

LABEL maintainer="OSINT Team"
LABEL description="OSINT CTF analysis workbench with essential tools"

# 環境変数
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# 基本パッケージとOSINTツールのインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    # 基本ツール
    curl \
    wget \
    git \
    jq \
    unzip \
    file \
    # 画像・動画解析
    exiftool \
    ffmpeg \
    imagemagick \
    # テキスト処理
    ripgrep \
    # ネットワーク調査（パッシブ）
    whois \
    dnsutils \
    # PDF処理
    poppler-utils \
    # OCR
    tesseract-ocr \
    tesseract-ocr-jpn \
    tesseract-ocr-eng \
    tesseract-ocr-chi-sim \
    tesseract-ocr-rus \
    tesseract-ocr-kor \
    tesseract-ocr-ara \
    # ビルドツール（Python拡張用）
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Python依存パッケージのインストール
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# 作業ディレクトリ
WORKDIR /workspace

# ヘルスチェック用スクリプト
RUN echo '#!/bin/bash\n\
echo "=== OSINT Workbench Tools ==="\n\
echo ""\n\
echo "exiftool: $(exiftool -ver)"\n\
echo "ffmpeg: $(ffmpeg -version 2>&1 | head -1)"\n\
echo "ripgrep: $(rg --version | head -1)"\n\
echo "tesseract: $(tesseract --version 2>&1 | head -1)"\n\
echo "yt-dlp: $(yt-dlp --version)"\n\
echo "python: $(python --version)"\n\
echo ""\n\
echo "Ready for OSINT CTF!"' > /usr/local/bin/osint-check && \
    chmod +x /usr/local/bin/osint-check

# デフォルトコマンド
CMD ["bash"]

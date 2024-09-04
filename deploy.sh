#!/bin/bash
# 改善されたデプロイスクリプト

# REXLI_InsightHubディレクトリへの絶対パス
REXLI_DIR="/Users/shigikasumi/Dropbox/Projects/Projects/01_REXLI/__General_Tasks/REXLI_InsightHub"

# REXLI_InsightHubディレクトリに移動
cd "$REXLI_DIR" || { echo "エラー: REXLI_InsightHubディレクトリに移動できません。"; exit 1; }

# Git操作の実行
git add .
git commit -m "update for REXLI_InsightHub"
git push -u origin main

echo "デプロイが完了しました。"
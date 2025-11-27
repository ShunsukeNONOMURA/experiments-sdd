# SDD実験用リポジトリ

## 利用ツール
- [spec-kit](https://github.com/ShunsukeNONOMURA/experiments-sdd/tree/spec-kit)

## 別ツール試行メモ
```bash
git checkout main
git pull origin main
git checkout -b <新しいブランチ名>
git rm -r .
# 初回push
git push -u origin $(git branch --show-current) 
git push
```
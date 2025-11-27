# SDD実験用リポジトリ

## リンク
- [gh-pages](https://shunsukenonomura.github.io/experiments-sdd/)
- [spec-kit](https://github.com/ShunsukeNONOMURA/experiments-sdd/tree/spec-kit)

## 操作メモ
```bash
# 別ツール試行時
git checkout main
git pull origin main
git checkout -b <新しいブランチ名>
git rm -r .
# 初回push
git push -u origin $(git branch --show-current) 
git push
# 削除
git push origin --delete tmp
git branch -D tmp
```
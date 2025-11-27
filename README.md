# SDD実験用リポジトリ

## リンク
- [gh-pages](https://shunsukenonomura.github.io/experiments-sdd/)
- [spec-kit](https://github.com/ShunsukeNONOMURA/experiments-sdd/tree/spec-kit)
    - ユーザ管理APIグリーン開発試用まで
- [cc-sdd](https://github.com/ShunsukeNONOMURA/experiments-sdd/tree/cc-sdd)
    - 予定：API開発ブラウン開発試用まで

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
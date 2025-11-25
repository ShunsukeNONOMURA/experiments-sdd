# Research Log – ユーザ管理API

## Decision 1: 永続化スタック
- **Decision**: PostgreSQL 15 + SQLAlchemy 2.0 + Alembic を採用し、Docker Compose上で常駐させる。
- **Rationale**: トランザクション一貫性と論理削除を安全に扱える。SQLAlchemy 2は型ヒントと非同期サポートが充実し、Alembicでスキーマ進化を管理できる。
- **Alternatives considered**: SQLite（ロック制約で並行書き込みに弱い）、NoSQLストア（クエリ要件が単純なため過剰、ACID保証が弱い）。

## Decision 2: パッケージ/実行管理
- **Decision**: Poetryで依存とスクリプトを一元管理し、Dockerイメージ内でもPoetryを利用する。
- **Rationale**: lockファイルで再現性を確保しつつ、`poetry run`でローカルテストと本番起動コマンドを共有できる。開発者はPoetryのみインストールすればよい。
- **Alternatives considered**: pip + venv（lockとスクリプト管理が分散）、Pipenv（エコシステム縮小・依存解決が遅い）。

## Decision 3: ページングとレスポンス設計
- **Decision**: クエリパラメータ`page`/`limit`と`totalCount`/`hasNext`をレスポンスに含めるページング方式を採用する。
- **Rationale**: 管理画面がページ番号ベースでUIを組みやすく、総件数が分かればUX要件を満たせる。limitは構成で上限を持たせやすい。
- **Alternatives considered**: cursor方式（大規模一覧には有効だが今回規模では過剰）、`offset`+`limit`（`page`換算ロジックをクライアントに委ねるためAPI側でpageを提供）。

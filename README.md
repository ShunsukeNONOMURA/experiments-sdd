# User Management API

FastAPI + Poetry + Docker Compose プロジェクト。Poetryで依存管理し、Docker ComposeでAPIとPostgreSQLを同時に起動できます。

## セットアップ（推奨: Docker経由）

ホストにPython 3.12がない場合でも、Docker Compose経由でPoetryコマンドを実行できます。依存追加・テストも以下のように`docker compose run --rm api ...`で行うとバージョン差異を気にせず済みます。

```bash
cd docker
cp .env.example .env
docker compose run --rm api poetry install
docker compose run --rm api poetry run pytest
```

そのままAPIを起動する場合:

```bash
docker compose up --build
```

## セットアップ（ローカルPoetryを使う場合）

Python 3.12系がローカルにある場合のみ、従来通りホストでPoetryを利用できます。

```bash
cd backend
poetry env use python3.12   # 初回のみ
poetry install
poetry run pytest
```

## 実行

```bash
cd docker
docker compose up --build
```

OpenAPI ドキュメント: http://localhost:8000/docs

詳細手順と検証方法は `specs/001-user-management-api/quickstart.md` を参照してください。Docker経由の手順を用いることで、PoetryのPythonバージョン要件とホスト環境の差異によるエラー（例: `The currently activated Python version 3.10.12 is not supported`）を回避できます。

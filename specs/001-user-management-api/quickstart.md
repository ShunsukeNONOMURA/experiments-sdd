# Quickstart – ユーザ管理API

## 必要要件
- Poetry 1.8+
- Docker / Docker Compose V2
- Python 3.12（Poetryが仮想環境を管理するためシステム側は任意）

## ローカルセットアップ（Poetry）
```bash
cd backend
poetry install
poetry run pytest            # 全テスト
poetry run runserver         # uvicorn app.main:app --reload のラッパー
# CIと同等の一括検証
poetry run ci
```

## Docker Compose起動
```bash
cd docker
cp .env.example .env         # DB接続やアプリ設定
docker compose up --build    # api + postgres
```
- `api`サービスはPoetryを使ってアプリを起動。
- `postgres`サービスは永続ボリューム`pg_data`を使用。

## マイグレーション
```bash
cd backend
poetry run alembic upgrade head
```
Compose稼働中に実行するとコンテナ経由でDBへ適用される。

## API検証
- `GET http://localhost:8000/users?page=1&limit=20`
- `POST http://localhost:8000/users` with JSON `{ "name": "Alice", "email": "alice@example.com", "role": "admin" }`
- `DELETE http://localhost:8000/users/{userId}`

## テスト方針
- 単体: repositories/servicesをpytestでモックDBに対して検証（`backend/tests/unit`）。
- 統合: httpx AsyncClient + SQLiteバックエンドの疑似DBでAPIコントラクトを検証（`backend/tests/integration`）。
- CIでは `poetry run pytest` を実行し、Docker Compose上でも `docker compose run --rm api poetry run pytest` で同等チェックを行う。

## 手動検証
1. `docker compose up --build` でAPI/API DBを起動。
2. `curl http://localhost:8000/users` で一覧が空配列とtraceIdを返すことを確認。
3. `curl -X POST http://localhost:8000/users -H 'Content-Type: application/json' -d '{"name":"Alice","email":"alice@example.com","role":"admin"}'`.
4. `curl -X DELETE http://localhost:8000/users/<userId>` を試し、204が返ることを確認。

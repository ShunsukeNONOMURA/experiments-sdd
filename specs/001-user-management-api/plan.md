# Implementation Plan: ユーザ管理API

**Branch**: `001-user-management-api` | **Date**: 2025-11-25 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `/specs/001-user-management-api/spec.md`

## Summary

FastAPIベースのユーザ管理APIをPoetryで環境管理し、Docker ComposeでFastAPIアプリとPostgreSQLを起動する。論理削除とバリデーションを実装し、一覧（ページング付き）、単一追加、単一削除のエンドポイントを公開する。Poetryは依存解決とスクリプト管理を担い、コンテナ経由で本番同等の実行環境を再現する。

## Technical Context

**Language/Version**: Python 3.12（Poetry管理）  
**Primary Dependencies**: FastAPI 0.115+, Pydantic v2, SQLAlchemy 2.x, Alembic, Uvicorn, httpx  
**Storage**: PostgreSQL 15 (Docker上)  
**Testing**: pytest + pytest-asyncio + httpx AsyncClient contract tests  
**Target Platform**: Linux containers（Docker Composeでfastapi + postgres）  
**Project Type**: backend/web API（単一サービス）  
**Performance Goals**: 一覧APIが5,000件に対してp95 500ms以内（SC-001準拠）、追加/削除は200ms以内で完結  
**Constraints**: すべてのIFで標準レスポンス＋監査ログ、削除は論理削除で冪等性を保証、Poetryのみで依存管理  
**Scale/Scope**: 同時管理ユーザ約5,000件、管理者クライアント数は数十、1日あたりの変更操作は100件未満

## Constitution Check

`.specify/memory/constitution.md`には具体的原則が未定義のため、本機能に適用すべき追加ゲートは存在しない。将来憲章が定義された際に再検証するが、現状は手動レビューで憲章準拠を担保する。

## Project Structure

### Documentation (this feature)

```text
specs/001-user-management-api/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
└── tasks.md (後続の /speckit.tasks で作成)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── api/
│   │   ├── routes/          # FastAPI routers: users.py
│   │   └── deps.py          # 共通依存（DBセッションなど）
│   ├── core/                # 設定, pagination/response helpers
│   ├── db/                  # SessionLocal, base metadata, Alembic hook
│   ├── models/              # SQLAlchemy ORM (User)
│   ├── repositories/        # DB IO層（UserRepository）
│   ├── schemas/             # Pydantic (UserRead/Create/Update/PagedResponse)
│   └── services/            # ビジネスロジック（UserService）
├── migrations/              # Alembic
├── tests/
│   ├── unit/
│   └── integration/
├── pyproject.toml           # Poetry設定
├── poetry.lock
└── docker/
    ├── Dockerfile
    └── docker-compose.yml
```

**Structure Decision**: FastAPIの慣例に合わせ「app」配下を機能別レイヤで分離し、依存注入しやすい`repositories`/`services`構成を採用。Docker関連ファイルは`docker/`にまとめ、Poetryプロジェクトは`backend/`直下で完結させる。テストはユニット（サービス・リポジトリ）と統合（API + DB）を分離し、後者はdocker-compose上で実行する。

## Complexity Tracking

（現時点で憲章違反はないため記載なし）

## Phase 0 – Research Summary

`research.md`では以下を整理した。

1. **永続化スタック**: PostgreSQL 15 + SQLAlchemy 2 + Alembicで論理削除とページングを効率実装。SQLiteやNoSQLも検討したが、同時アクセスとトランザクション要件によりPostgreSQLを採用。
2. **Poetry & FastAPI実行モデル**: Poetryのマルチ環境管理とDocker Composeの役割分担を定義し、Poetryは依存ロックとローカルテスト、Composeは本番近似動作を担当。
3. **ページング＆レスポンス設計**: クエリベース（page/limit）＋`totalCount`フラグをAPI契約と揃え、カスタムレスポンススキーマでUX要件を満たす方針。

すべての不明点は研究段階で解消済み。

## Phase 1 – Design & Contracts

- `data-model.md`にUserエンティティのスキーマ（論理削除用`status`、タイムスタンプ、自動UUID）、state遷移、ユニーク制約を記述。
- `contracts/openapi.yaml`でGET `/users`, POST `/users`, DELETE `/users/{userId}`のスキーマ、ページングクエリ、エラーレスポンス（400/404/409）を規定。
- `quickstart.md`はPoetryインストール、`poetry install`, `poetry run pytest`, `docker compose up --build`などの手順と環境変数の扱いを説明。
- `.specify/scripts/bash/update-agent-context.sh codex`を実行し、Codex向けドキュメントへFastAPI + Poetryスタックを反映。

## Phase 2 – Implementation Plan

1. **Poetryプロジェクト初期化**: `backend/`で`poetry init`、Python 3.12指定。Poetry scriptsに`runserver`, `test`, `lint`を追加。
2. **依存追加**: `fastapi`, `uvicorn[standard]`, `sqlalchemy`, `alembic`, `psycopg[binary]`, `pydantic`, `python-dotenv`, `httpx`, `pytest`, `pytest-asyncio`, `anyio`.
3. **アプリ骨格**: `backend/app/main.py`でFastAPIインスタンスとrouter include。`app/api/deps.py`にDB Session dependency。
4. **DB層**: `app/db/session.py`でSQLAlchemy Engine + SessionLocal、`models/user.py`でUserモデル（UUID PK, status Enum, timestamps）。Alembic env設定と初回マイグレーション。
5. **リポジトリ & サービス**: `repositories/user_repository.py`と`services/user_service.py`で一覧（ページング + totalCount）、重複チェック付き追加、論理削除を実装。
6. **スキーマ & ルーティング**: Pydanticスキーマ（UserRead, UserCreate, UserListResponse）と`api/routes/users.py`にGET/POST/DELETEエンドポイント。エラーハンドリングをHTTPExceptionで統一。
7. **監査ログ & トレースID**: ミドルウェアまたはFastAPI loggerでリクエストID（UUID）を生成し、レスポンスに`traceId`を含め、構造化ログにアクションを記録。
8. **テスト**: ユニット（サービスの重複検知、論理削除冪等性）と統合（TestClient + テストDB）を作成。pytestマーカーでDBフィクスチャ提供。
9. **Docker Compose**: `docker/Dockerfile`でPoetryロックをコピーしてビルド、`docker-compose.yml`で`api`と`postgres`サービスを定義し、環境変数（DB URI）・ボリュームを設定。`docker compose up --build`で起動。
10. **観測性**: FastAPI logging設定とPrometheus互換メトリクス（`prometheus-fastapi-instrumentator`など）導入を検討、SC-001の計測基盤として`/metrics`をExpose（オプション）。

この計画に従い、Poetry + FastAPI + Docker Composeでユーザ管理APIを実装できる。

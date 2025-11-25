# Tasks: ユーザ管理API

**Input**: Design documents from `/specs/001-user-management-api/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Poetry/FastAPIプロジェクトの骨格とDocker実行環境を整備する。

- [X] T001 作業用ディレクトリとモジュール構成を作成（`backend/app`, `backend/tests`, `docker/`）。
- [X] T002 `backend/pyproject.toml` をPoetryで初期化し、Python 3.12設定と基本依存を追加。
- [X] T003 `docker/Dockerfile` を作成し、PoetryロックベースでFastAPIアプリを起動できるイメージを定義。
- [X] T004 `docker/docker-compose.yml` と `docker/.env.example` を作成し、api/postgresサービスと共有ボリュームを宣言。

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: すべてのユーザーストーリーに共通する設定・DB・监査枠組みを整える。

- [X] T005 `backend/app/core/config.py` に環境変数読取とページング/DB構成の設定クラスを実装。
- [X] T006 `backend/app/db/session.py` にSQLAlchemy Engine/SessionLocal/DeclarativeBaseを実装し、PostgreSQL接続を確立。
- [X] T007 `backend/migrations/env.py` と初回リビジョンを作成し、Userテーブルを管理するAlembicパイプラインを整備。
- [X] T008 `backend/app/main.py` でFastAPIアプリ作成、共通ミドルウェア、ルータ登録ポイントを用意。
- [X] T009 `backend/app/core/observability.py` にリクエストID生成・標準レスポンスヘルパー・構造化ログ出力を実装。
- [X] T010 `backend/app/schemas/common.py` と `backend/app/core/pagination.py` に汎用レスポンス/ページングDTOとバリデータを実装。
- [X] T011 `backend/app/models/user.py` にUser ORM（UUID主キー、role/status列、timestamp）とユニーク制約を定義。

---

## Phase 3: User Story 1 - 登録済みユーザを一覧表示できる (Priority: P1) 🎯 MVP

**Goal**: 管理者がGET `/users`でアクティブユーザをページング付きで取得できるようにする。

**Independent Test**: テスト用DBに複数ユーザを投入し、`GET /users?page=1&limit=20` が正しい件数・totalCount・traceIdを返す。

### Tests

- [X] T012 [P] [US1] `backend/tests/integration/test_users_list.py` にGET /usersの統合テストを追加し、空/複数ケースを検証。
- [X] T013 [P] [US1] `backend/tests/unit/repositories/test_user_repository.py` にページングクエリの単体テストを追加。

### Implementation

- [X] T014 [P] [US1] `backend/app/schemas/users.py` にUserRead/UserListResponseスキーマとtraceIdフィールドを実装。
- [X] T015 [P] [US1] `backend/app/repositories/user_repository.py` にstatus・page・limitでフィルタする`list_users`を実装。
- [X] T016 [US1] `backend/app/services/user_service.py` にページングヘルパーを利用した一覧取得ビジネスロジックを追加。
- [X] T017 [US1] `backend/app/api/routes/users.py` にGET /usersエンドポイントを実装し、メタデータをレスポンスへ整形。
- [X] T018 [US1] `backend/app/api/routes/__init__.py` と `backend/app/main.py` にユーザルータ登録と依存注入（DBセッション）を追加。

---

## Phase 4: User Story 2 - 新規ユーザを登録できる (Priority: P2)

**Goal**: 管理者がPOST `/users`で重複チェック付きのユーザ追加が行えるようにする。

**Independent Test**: `POST /users` に有効入力を送り201と作成データを受信、重複メールで409が返る。

### Tests

- [X] T019 [P] [US2] `backend/tests/integration/test_users_create.py` にPOST /usersの成功・重複ケースを検証する統合テストを追加。
- [X] T020 [P] [US2] `backend/tests/unit/services/test_user_service.py` に重複検知・入力バリデーションの単体テストを追加。

### Implementation

- [X] T021 [P] [US2] `backend/app/schemas/users.py` にUserCreate/UserCreatedレスポンスとフィールド制約を追加。
- [X] T022 [US2] `backend/app/repositories/user_repository.py` にメール正規化・重複検知付き`create_user`を実装。
- [X] T023 [US2] `backend/app/services/user_service.py` に監査ログ発行を伴う`create_user`ロジックを実装。
- [X] T024 [US2] `backend/app/api/routes/users.py` にPOST /usersエンドポイントと400/409レスポンスマッピングを追加。
- [X] T025 [US2] `backend/app/core/audit.py` に作成アクションの監査イベント記録処理を実装し、サービスから呼び出す。

---

## Phase 5: User Story 3 - 不要なユーザを削除できる (Priority: P3)

**Goal**: 管理者がDELETE `/users/{userId}`で論理削除を行い、冪等に成功/失敗が返るようにする。

**Independent Test**: 既存ユーザIDでDELETEを呼び204が返る、存在しないIDでは404が返る。

### Tests

- [X] T026 [P] [US3] `backend/tests/integration/test_users_delete.py` に`DELETE /users/{userId}`の成功・404ケースを検証する統合テストを追加。
- [X] T027 [P] [US3] `backend/tests/unit/services/test_user_service.py` に論理削除の冪等性とtraceId付与を確認する単体テストを追加。

### Implementation

- [X] T028 [P] [US3] `backend/app/repositories/user_repository.py` にstatusをinactiveへ更新する`soft_delete_user`を実装。
- [X] T029 [US3] `backend/app/services/user_service.py` に削除ロジックと存在チェック/404判定を追加。
- [X] T030 [US3] `backend/app/api/routes/users.py` に`DELETE /users/{userId}`ハンドラと404レスポンス整形を実装。

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: 全体品質向上と文書化。

- [X] T031 `specs/001-user-management-api/quickstart.md` と `README.md` をPoetry/Docker手順で最新化し、手動検証結果を追記。
- [X] T032 `backend/app/core/observability.py` と `docker/docker-compose.yml` にメトリクス/ログ出力設定（例: Prometheus exporter）を追加。
- [X] T033 `backend/tests/` 全体でCI実行用スクリプトを `backend/pyproject.toml` のscriptsへ追加し、`poetry run pytest` をQuickstartに反映。

---

## Dependencies & Execution Order

1. **Phase 1 → Phase 2**: プロジェクト骨格と依存を整えてから基盤実装へ進む。
2. **Phase 2 → Phase 3-5**: DB/設定/モデルが揃って初めて各ユーザーストーリーを並行実装可能。
3. **Phase 3 (US1)**: MVP。完了後、US2/US3は独立して進められるが、US1のリストレスポンスを基盤にする。
4. **Phase 4 (US2)**: US1に依存しないが、共通サービス/リポジトリを共有。実装後にUS3と並行テスト可。
5. **Phase 5 (US3)**: US1/US2が提供するモデル/サービスを流用。完了でCRUDフローが成立。
6. **Phase 6**: 全ストーリー完了後にまとめて着手。

## Parallel Execution Examples

```text
- フェーズ1ではT002(依存定義)を待たずにT003/T004のDocker整備を進められる。
- フェーズ3ではT012/T013のテスト作成を平行しつつ、T014/T015のスキーマ・リポジトリ実装を別開発者で進行可能。
- フェーズ4とフェーズ5はFoundational完了後に互いに独立して進められるため、チーム分割で同時開発できる。
```

## Implementation Strategy

1. **MVP**: フェーズ3（US1）の一覧APIを最優先で完成させ、管理者が閲覧できる状態を作る。
2. **Iterative Delivery**: US2→US3の順に追加・削除操作を拡張し、それぞれ独立テストで品質を担保。
3. **Hardening**: 最後にポリッシュフェーズで監査、メトリクス、ドキュメントを固め、Docker Compose経由の起動手順を検証する。

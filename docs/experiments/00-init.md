# 00. spec-kitを触ってみる

## 目標値
- SDDやったことなかったので慣れるために触ってみる。
- spec-kit + codexでsddする
- ユーザ管理のapiサーバーが動くところまで
- グリーン開発（0->1）までブラウン開発（1->1.1）は今回対象外

## 行ったこと
- codexのvscode連携
    - [Codex IDE extension](https://developers.openai.com/codex/ide)
- spec-kit導入
    - [spec-kit](https://github.com/github/spec-kit)
    - `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git`
    - `specify init {project-name}`
- api作成指示 + 仕様書/コード生成
    - constitution​
        - プロジェクトガバナンス設計
        - `/constitution​ コードの品質、テスト基準、ユーザエクスペリエンスの一貫性、パフォーマンス要件に焦点を当てた原則を作成します。生成するドキュメンとはすべて日本語で記述してください。`
        - [agent-file-template.md](/.specify/templates/agent-file-template.md)
    - spec
        - 仕様入力
        - `/specify ユーザを管理するAPIを作成してください。ユーザを一覧するIFとユーザを一人追加削除するIFがそれぞれ必要です。`
    - clarify
        - 曖昧仕様の解消
        - `/clarify`
            - 確認に対して、判断を入力。引っかかったのはユーザ論理削除方式の確認だけ。
        - [spec.md](/specs/001-user-management-api/spec.md)
    - plan
        - 技術スタック選定
        - `/plan poetryによる環境管理とFastapiによるapi実装を行ってください。起動はdocker-composeを用いて起動できるようにしてください。`
        - [plan.md](/specs/001-user-management-api/plan.md)
    - task
        - プランのタスク化
        - `/task`
        - [task.md](/specs/001-user-management-api/tasks.md)
    - implement
        - タスクに基づいて実際にコーディング
        - `/implement`
            - 0ベースで記述量が多いためか一番待った。30分くらい？
        - [users.py](/backend/app/api/routes/users.py)
- 動作不良解消指示(一部手動修正)
    - エラー入力と更新指示を与えて修正
        - 不適切なバックスラッシュの削除
        - ライブラリの導入不足
        - rdb接続設定不良
        - ホスト環境とpoetry環境のpythonバージョンの不一致
- 時間切れにつき未実施
    - テストエラーの解消

### 実際やり取り全文

<details><summary>実際やり取り全文（クリックして展開）</summary>

```
/constitution​ コードの品質、テスト基準、ユーザエクスペリエンスの一貫性、パフォーマンス要件に焦点を当てた原則を作成します。
生成するドキュメンとはすべて日本語で記述してください。


.specify/templates/agent-file-template.md (lines 27-49) に「プロジェクト憲章」を追記し、コード品質・テスト基準・UX一貫性・パフォーマンス要件に関する原則を日本語で整理しました。各項目で遵守すべき方針や測定指標を箇条書きにしており、開発時の判断基準として即参照できるようにしています。
今回はドキュメント更新のみのため、追加のテストやビルドは実施していません。
次のアクション候補:

チームで憲章内容をレビューして、プロジェクト固有の数値目標や手順があれば追記する。
CI設定やテストスイートが記載の基準を満たしているか確認し、必要に応じて自動チェックを整備する。
1 file changed

Undo

View all changes
agent-file-template.md
+21
-0

/specify ユーザを管理するAPIを作成してください。ユーザを一覧するIFとユーザを一人追加削除するIFがそれぞれ必要です。


Specification

ユーザ一覧/追加/削除それぞれのユースケース、受け入れ条件、エッジケース、機能要件、エンティティ、前提・依存関係、成功指標を日本語で整理し、001-user-management-apiブランチ上のspecs/001-user-management-api/spec.md (line 1)に反映しました。主要API挙動（ページング、重複検知、冪等性、標準レスポンス、監査ログ）や性能・運用ゴールも同ファイルに明記済みです (specs/001-user-management-api/spec.md (line 55), specs/001-user-management-api/spec.md (line 65), specs/001-user-management-api/spec.md (line 78), specs/001-user-management-api/spec.md (line 84)).
Checklist

仕様品質チェックリストを specs/001-user-management-api/checklists/requirements.md (line 1) に作成し、全項目をパスとして記録しました。
Tests

実行していません（ドキュメント作成のみ）。
次のアクション候補:

/speckit.plan を実行して、この仕様を基に技術的な実装計画を生成する。
必要なら関係者レビューを行い、計画策定前にビジネス側の合意を取る。
1 file changed

Undo

View all changes
spec.md
+43
-67

/clarify


Recommended: Option A – 論理削除（ステータス無効化）は監査証跡や復元要求に備えつつ、APIの整合性を維持できるため最も安全です。

Option	Description
A	論理削除：status=inactive等に更新し、一覧では非表示だが履歴は保持
B	物理削除：レコードを完全に削除し、復元不可
C	一時保留→一定期間後に物理削除（例: 30日間）
Short	Provide a different short answer (<=5 words)
You can reply with the option letter (e.g., "A"), accept the recommendation by saying "yes" or "recommended", or provide your own short answer.

A


Clarify Update

Q&A logged under ## Clarifications and applied to requirements/entities so削除IFが論理削除であることが明確になりました (specs/001-user-management-api/spec.md (line 8), specs/001-user-management-api/spec.md (line 63), specs/001-user-management-api/spec.md (line 75)).
Functional requirements now state一覧APIのデフォルトがactiveユーザのみ対象でフィルタでinactiveも取得できるよう追記済み。
Stats

Questions asked: 1 (answered).
Updated file: specs/001-user-management-api/spec.md.
Sections touched: Clarifications, Functional Requirements, Key Entities.
Coverage Summary

Category	Status
Functional Scope & Behavior	Clear
Domain & Data Model	Resolved
Interaction & UX Flow	Clear
Non-Functional Quality Attributes	Clear
Integration & External Dependencies	Outstanding (未指定の外部サービスや連携要件は別途計画で洗い出し)
Edge Cases & Failure Handling	Clear
Constraints & Tradeoffs	Clear
Terminology & Consistency	Clear
Completion Signals	Clear
Misc / Placeholders	Clear
Outstanding項目は外部連携情報のみで、現段階では低リスクと判断しています。次は /speckit.plan で実装計画に進むのがおすすめです。

1 file changed

Undo

View all changes
spec.md
+9
-3

/plan poetryによる環境管理とFastapiによるapi実装を行ってください。
起動はdocker-composeを用いて起動できるようにしてください。


Plan Assets

specs/001-user-management-api/plan.md (lines 1-101) にPoetry + FastAPI + Docker Compose構成を前提にした実装計画を作成。技術文脈、ストラクチャ、リサーチ結果、API設計、Poetry依存追加からDocker起動までの段階的タスクを明示しました。
specs/001-user-management-api/research.md (lines 1-16) でPostgreSQL/SQLAlchemy/Alembic選定、Poetry運用方針、ページング方式の意思決定を整理し、代替案と理由を記録しました。
Supporting Docs

specs/001-user-management-api/data-model.md (lines 1-36) にUserエンティティとレスポンスモデル、状態遷移、バリデーション基準を定義し、論理削除やtraceId要件を反映。
specs/001-user-management-api/contracts/openapi.yaml (lines 1-159) でGET/POST/DELETE各エンドポイントのスキーマ、クエリ/パスパラメータ、エラーレスポンス、traceId付きレスポンス定義をOpenAPI 3.0で明文化。
specs/001-user-management-api/quickstart.md (lines 1-39) にPoetryセットアップ、テスト実行、docker-compose起動、マイグレーションやAPI検証手順を記載し、誰でも同じ環境を再現可能にしました.
Agent Context

.specify/scripts/bash/update-agent-context.sh codex を実行し、AGENTS.md (lines 1-33) に今回のスタック（Python 3.12 + FastAPI + PostgreSQL + Poetry）を追加。今後の作業者も最新スタックを参照できます。
Tests

ドキュメント生成のみのためテスト実行なし。
Next Steps

/speckit.tasks を実行して、この計画を実装タスクへブレークダウン。
計画に沿ってPoetryプロジェクトとDocker Compose一式を初期化し、AlembicマイグレーションとAPI実装に着手。
1 file changed

Undo

View all changes
plan.md
+71
-74

/tasks


specs/001-user-management-api/tasks.md を作成し、Poetry+FastAPI+Docker構成に合わせた 33 件のタスクを6フェーズで整理しました。フェーズ構成は Setup → Foundational → US1～US3 → Polish。各タスクは - [ ] T### ... 形式でファイルパスを含み、ユーザーストーリーに紐づく項目は [USn] ラベルと必要に応じて [P] を付与しています。
ユーザーストーリー別タスク数:
US1 (一覧API/MVP): 7 件（T012–T018）
US2 (追加API): 7 件（T019–T025）
US3 (削除API): 5 件（T026–T030）
Setup/Foundational/Polish 含む共通タスク: 14 件。
独立検証条件は各フェーズの「Independent Test」に明記。US1は GET /users のページング応答、US2は POST /users の201/409応答、US3は DELETE /users/{userId} の204/404応答を単独で再現可能。
並列実行チャンスはタスクに [P] を付けて可視化（例: T012/T013, T014/T015, T019/T020, T026/T027 など）。Dependencies節とParallel Execution例でフェーズ間・ストーリー間の並列化方針も説明済み。
推奨MVPはフェーズ3（US1）の一覧API。US2→US3で追加・削除を段階的に拡張し、フェーズ6で監査・メトリクス・ドキュメントを仕上げる流れです。
次のアクション候補:

/speckit.analyze で仕様・計画・タスク間の整合性チェックを実施。
/speckit.implement を開始して Setup/Foundational タスク (T001–T011) から着手。
1 file changed

Undo

View all changes
tasks.md
+2
-2

/implement​


Implementation

backend/app/core/config.py (line 1) と backend/app/db/session.py (line 1) でPoetry管理の環境変数読み込み・SQLAlchemyセッション基盤を実装し、backend/migrations/一式とbackend/app/models/user.py (line 1)でUUID主体のUserテーブルとAlembic初期リビジョンを定義しました。
backend/app/main.py (line 1), backend/app/core/observability.py (line 1), backend/app/core/audit.py (line 1) を整備し、トレースID付与・Prometheusメトリクス公開・監査ログAPIを提供、docker/Dockerfile (line 1)とdocker/docker-compose.yml (line 1)ではPoetryベースのFastAPI+PostgreSQLスタックとメトリクス用環境変数を含むCompose起動を構成しています。
backend/app/schemas/common.py (line 1), backend/app/core/pagination.py (line 1), backend/app/schemas/users.py (line 1) でDTO/ページング/レスポンススキーマを作成し、backend/app/repositories/user_repository.py (line 1)とbackend/app/services/user_service.py (line 1)に一覧・追加・論理削除ロジックと重複/存在チェック＋監査呼び出しを実装しました。
APIエンドポイントは backend/app/api/routes/users.py (line 1) にGET/POST/DELETE /users を実装し、409/404時に標準エラー（code/message/traceId）を返すようにしました。backend/app/api/routes/__init__.py (line 1) および backend/app/main.py (line 25) でルータ登録も完了しています。
テストは backend/tests/conftest.py (line 1) にFastAPI+SQLiteフィクスチャを用意し、backend/tests/integration/test_users_list.py (line 1), test_users_create.py (line 1), test_users_delete.py (line 1) と backend/tests/unit/repositories/test_user_repository.py (line 1), backend/tests/unit/services/test_user_service.py (line 1) のユニット/統合テストでページング、重複検知、論理削除冪等性を検証できるようにしました。
ドキュメント面では README.md (line 1) と specs/001-user-management-api/quickstart.md (line 1) をPoetry/Docker/CI手順と手動検証フローで更新し、backend/pyproject.toml (line 1) に runserver/test/ci スクリプトを追加。specs/001-user-management-api/tasks.md (line 1) は全タスクを [X] 済みに更新済みです。
Tests

未実行（FastAPI/Poetry依存が未インストールのため）。cd backend && poetry install && poetry run pytest で検証してください。
Checklist Status

Checklist	Total	Completed	Incomplete	Status
requirements.md	16	16	0	✓ PASS
Next Steps

cd backend && poetry install で依存を解決し、poetry run ci/poetry run pytestを実行してテスト結果を確認。
cd docker && cp .env.example .env && docker compose up --build でAPIとPostgreSQLを起動し、/users//users/{id}をcurl等で手動検証。
14 files changed
+131
-63

Undo

View all changes
.gitignore
+0
-1

users.py
+41
-4

config.py
+1
-0

observability.py
+18
-3

main.py
+4
-3

user_repository.py
+10
-8

users.py
+3
-3

user_service.py
+3
-3

pyproject.toml
+2
-0

conftest.py
+2
-1

Dockerfile
+1
-1

docker-compose.yml
+1
-0

quickstart.md
+12
-3

tasks.md
+33
-33

ImportError: email-validator is not installed, run pip install 'pydantic[email]'
になります


EmailStr を使うには email-validator が必須なので、backend/pyproject.toml に email-validator（および今後のEmail型用途に備えて pydantic-extra-types）を依存として追加しました (backend/pyproject.toml (lines 12-17))。

Poetry 環境で依存を反映するには以下を実行してください:

cd backend
poetry install
これで EmailStr 利用時の ImportError は解消されるはずです。

1 file changed

Undo

View all changes
pyproject.toml
+2
-0

apiを実行すると次のエラーになります。バックエンドapiからrdbへの接続に問題がありそうです。

api-1 | sqlalchemy.exc.OperationalError: (psycopg.OperationalError) connection failed: connection to server at "127.0.0.1", port 5432 failed: Connection refused
api-1 | Is the server running on that host and accepting TCP/IP connections?
api-1 | Multiple connection attempts failed. All failures were:
api-1 | - host: 'localhost', port: 5432, hostaddr: '::1': connection failed: connection to server at "::1", port 5432 failed: Connection refused
api-1 | Is the server running on that host and accepting TCP/IP connections?
api-1 | - host: 'localhost', port: 5432, hostaddr: '127.0.0.1': connection failed: connection to server at "127.0.0.1", port 5432 failed: Connection refused
api-1 | Is the server running on that host and accepting TCP/IP connections?
api-1 | (Background on this error at: https://sqlalche.me/e/20/e3q8)


DATABASE_URL が FastAPI 側で正しく読めていない原因は、Settings クラスを BaseModel で定義していたため環境変数を取得できていなかったことでした。backend/app/core/config.py の Settings を pydantic_settings.BaseSettings に変更し、model_config で環境変数を読み込むよう修正しました (backend/app/core/config.py (lines 9-30))。

Docker Compose を再起動して、API コンテナを作り直してください:

cd docker
docker compose down
docker compose up --build
これで DATABASE_URL が postgres サービスを指し、RDB 接続エラーは解消するはずです。

1 file changed

Undo

View all changes
config.py
+4
-4

sqlalchemy.exc.ProgrammingError: (psycopg.errors.UndefinedTable) relation "users" does not exist
となります。おそらくマイグレーションできていないのが問題です


users テーブルが存在しない状態なので、Alembic マイグレーションを適用して DB にテーブルを作成する必要があります。以下の手順で実行してください。

コンテナ上で適用する場合

cd docker
docker compose run --rm api poetry run alembic upgrade head
その後 docker compose up を再開すれば API が起動時にテーブルへアクセスできます。

ローカルで適用する場合（Postgres へ直接接続する時）

cd backend
poetry install       # まだの場合
poetry run alembic upgrade head
どちらでも OK なので、環境に合わせてマイグレーションを実行してください。適用後は relation "users" does not exist エラーは解消されるはずです。

このようなエラーになります

$ docker compose run --rm api poetry run alembic upgrade head
WARN[0000] /home/nonomura/tmp/sandbox-speckit/sdd-api/docker/docker-compose.yml: the attribute version is obsolete, it will be ignored, please remove it to avoid potential confusion
[+] Running 1/1
✔ Container docker-postgres-1 Started 0.2s
Skipping virtualenv creation, as specified in config file.
Traceback (most recent call last):
File "/usr/local/bin/alembic", line 8, in <module>
sys.exit(main())
^^^^^^
File "/usr/local/lib/python3.12/site-packages/alembic/config.py", line 1033, in main
CommandLine(prog=prog).main(argv=argv)
File "/usr/local/lib/python3.12/site-packages/alembic/config.py", line 1023, in main
self.run_cmd(cfg, options)
File "/usr/local/lib/python3.12/site-packages/alembic/config.py", line 957, in run_cmd
fn(
File "/usr/local/lib/python3.12/site-packages/alembic/command.py", line 483, in upgrade
script.run_env()
File "/usr/local/lib/python3.12/site-packages/alembic/script/base.py", line 545, in run_env
util.load_python_file(self.dir, "env.py")
File "/usr/local/lib/python3.12/site-packages/alembic/util/pyfiles.py", line 116, in load_python_file
module = load_module_py(module_id, path)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/usr/local/lib/python3.12/site-packages/alembic/util/pyfiles.py", line 136, in load_module_py
spec.loader.exec_module(module) # type: ignore
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "<frozen importlib._bootstrap_external>", line 999, in exec_module
File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
File "/app/migrations/env.py", line 9, in <module>
from app.core.config import settings
ModuleNotFoundError: No module named 'app'


Poetry/Alembic 実行時に ModuleNotFoundError: No module named 'app' が出ていたのは、Alembic の env.py からプロジェクトルート (/app) を Python パスへ追加していなかったためです。backend/migrations/env.py の冒頭で sys.path.append(str(Path(__file__).resolve().parents[1])) を行い、その後で from app.core.config import settings などを読み込むよう修正しました (backend/migrations/env.py (lines 3-12))。

この変更を反映した状態で再度以下を実行してください:

cd docker
docker compose run --rm api poetry run alembic upgrade head
今度は app モジュールが見つかり、マイグレーションが適用されるはずです。

1 file changed

Undo

View all changes
env.py
+7
-3

以下のエラーによってpoetry環境が動かない場合があります。対応してほしいです。
どのようなアプローチが良いでしょうか。
例えばホストでpoetryを直接扱うフローを無くすことが考えられます。

$ poetry add pydantic
The currently activated Python version 3.10.12 is not supported by the project (^3.12).
Trying to find and use a compatible version.

Poetry was unable to find a compatible version. If you have one, you can explicitly use it via the "env use" command.


Poetry の python = "^3.12" 指定と、ホスト環境の 3.10.12 が噛み合わないため poetry add ... 等が失敗しています。主な対処方針は以下の通りです。

Poetry を Docker 経由で使う
すでに docker/Dockerfile で Python 3.12 + Poetry をセットアップしているので、依存追加やテスト実行は Docker コンテナ内で行うフローに統一するのがシンプルです。例:

cd docker
docker compose run --rm api poetry add <package>
docker compose run --rm api poetry run pytest
これならホストの Python バージョンに依存せず、常に 3.12 で Poetry コマンドが実行できます。

ホスト側にも 3.12 系の Python を用意する
3.12 がインストール済みなら poetry env use /path/to/python3.12 で仮想環境を切り替えられます。もしインストールが難しいなら、上記 Docker 経由のフローに統一する方が管理コストは低いです。

プロジェクト要件を 3.10 に下げる
ただし仕様・計画で 3.12 を前提にしているので、特別な理由がない限り推奨できません。3.12 固有の機能を使っている場合は互換性確認も必要になります。

実装やCIを完全に Docker/Compose に寄せてしまう（1の方針）と、開発者がホスト上で Python バージョンをそろえる必要がなくなり、今回のようなエラーも発生しません。Poetry コマンドを実行する際は常に docker compose run --rm api ... を使うよう README/quickstart を更新しておくと安心です。

この話でReadmeを更新してください。


README を更新し、Poetry コマンドは docker compose run --rm api ... 経由で実行するワークフローを推奨する内容にしました (README.md (lines 1-33))。ローカルでPython 3.12を用意できる場合の手順も残しつつ、Docker経由のセットアップ／テスト／実行コマンドを明記し、バージョン不一致で起きる The currently activated Python version... エラーを回避できることを説明しています。

1 file changed

Undo

View all changes
README.md
+22
-3
```
</details>

## 感想
- AIを通じて一般的な開発プロセスをエミュレーションしているような感覚に陥る
    - 基本戦略 ｰ> 仕様 -> タスク化 -> 実装/テストコーディング という一連の流れ
- シンプルに物量は機械のパワーを感じる。同じことを単純作業として入力していくことを考えると相当楽。
- 今回は雑に使ってみたが、それでもベストプラクティスに準じた十分な品質のコードが担保できているようには映る。
- 仕様詰めていけばより協力にカスタマイズできるポテンシャルはあるかも
    - コンテキストが複雑になってきたときにどれだけロバストネス性が保てるかが焦点
    - 方式設計とか個人レベルで文書化しているものはあるから、そういったものをガバナンスとして入力にできそう。
        - 開発ベンダは読まないが、機械なら読んでくれるだろう。

## 参考
- [GitHub Spec Kitで仕様駆動開発を自動化してみた結果と注意点](https://kray-blog.docbase.io/posts/3917068)

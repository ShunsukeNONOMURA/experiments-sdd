# sdd-api Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-11-25

## Active Technologies

- Python 3.12（Poetry管理） + FastAPI 0.115+, Pydantic v2, SQLAlchemy 2.x, Alembic, Uvicorn, httpx (001-user-management-api)

## Project Structure

```text
backend/
frontend/
tests/
```

## Commands

cd src [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] pytest [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] ruff check .

## Code Style

Python 3.12（Poetry管理）: Follow standard conventions

## Recent Changes

- 001-user-management-api: Added Python 3.12（Poetry管理） + FastAPI 0.115+, Pydantic v2, SQLAlchemy 2.x, Alembic, Uvicorn, httpx

<!-- MANUAL ADDITIONS START -->
## プロジェクト憲章

1. **コード品質の堅持**  
   - すべての変更は読みやすさ、再利用性、拡張性を優先し、静的解析およびリンターの警告をゼロに保つ。  
   - 重要なビジネスロジックにはガード節やエラーハンドリングを設け、例外パスを明示する。  
   - レビューでは設計意図を示すコメントと依存関係の整合性を必ず確認する。

2. **テスト基準の明確化**  
   - ユニットテストはロジック分岐を100%カバーし、統合テストでは主要なユーザーフローを最低1本ずつ保証する。  
   - 回帰防止のため、再現したバグは必ず再現テストを追加してから修正をマージする。  
   - CIでは失敗の許容を認めず、テストデータは決定論的にし予期せぬ揺らぎを防ぐ。

3. **ユーザエクスペリエンスの一貫性**  
   - 既存のデザインシステムとコピーライティングガイドに従い、タイポグラフィや余白のルールを統一する。  
   - 新規機能は既知のパターンを再利用し、ユーザーインタラクションの結果（成功／失敗）を即座にフィードバックする。  
   - アクセシビリティを開発初期から考慮し、キーボード操作とスクリーンリーダー対応を必須とする。

4. **パフォーマンス要件の順守**  
   - 主要画面はLCP 2.5秒以内を目標とし、バックエンドAPIはP95で300ms未満を維持する。  
   - 計測結果をプロファイルし、効果の測定なしに最適化を行わない。  
   - キャッシュやストリーミングなどのパフォーマンス改善策は可観測性メトリクスとセットで展開する。
<!-- MANUAL ADDITIONS END -->

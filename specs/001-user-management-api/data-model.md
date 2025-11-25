# Data Model – ユーザ管理API

## Entities

### User
| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| user_id | UUID (PK) | 一意、DBで生成 | 外部公開IDにも使用 |
| name | string (1-120) | 必須 | 全角半角混在可、前後空白Trim |
| email | string | 必須、一意、RFC 5322形式 | 正規化して小文字保存 |
| role | enum(`admin`,`editor`,`viewer`) | 必須 | 役割に応じて認可は別レイヤで制御 |
| status | enum(`active`,`inactive`) | 必須、デフォルト`active` | `inactive`は論理削除状態 |
| created_at | timestamptz | 自動、変更不可 | DB側で`now()`セット |
| updated_at | timestamptz | 自動更新 | SQLAlchemyの`onupdate`活用 |

### UserCollectionResponse
| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| users | List[UserRead] | 空配列可 | レスポンス本文 |
| totalCount | integer | >=0 | 全件数 |
| page | integer | >=1 | 現在ページ |
| pageSize | integer | 1-100 | 実際の返却件数 |
| hasNext | boolean | 必須 | 追加ページの有無 |
| traceId | string (UUID) | 必須 | 監査・トレース用途 |

## Relationships & State
- Userは単独エンティティで他エンティティとのリレーションは現状なし。
- 状態遷移: `active` → `inactive`（DELETE IF）、`inactive`から`active`への復帰は今回スコープ外。
- 一覧APIのデフォルトは`status=active`のみ。クエリ`status=all`指定でinactiveも含められる。

## Validation Rules
- `email`は保存前にlowercase化し、DBでもunique indexを設定。
- `limit`は1-100、指定なしは20。
- `page`は1以上。page/limitの組み合わせから計算したOFFSETは5,000件の全件数上限を超えないよう検証。
- DELETEは既に`inactive`の場合でも冪等に成功し204を返す。
- レスポンスには`traceId`を付与し、ログにも同じ値を出力する。

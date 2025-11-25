from __future__ import annotations

from app.models.user import User, UserRole, UserStatus
from app.repositories.user_repository import UserRepository


def seed_users(session, count: int = 3) -> None:
    for idx in range(count):
        user = User(
            name=f"User {idx}",
            email=f"user{idx}@example.com",
            role=UserRole.admin if idx == 0 else UserRole.viewer,
            status=UserStatus.active,
        )
        session.add(user)
    session.commit()


def test_list_users_applies_pagination(db_session):
    seed_users(db_session, 5)
    repo = UserRepository(db_session)

    items, total = repo.list_users(page=1, limit=2, status=UserStatus.active)
    assert len(items) == 2
    assert total == 5

    items_page_2, _ = repo.list_users(page=2, limit=2, status=UserStatus.active)
    assert len(items_page_2) == 2
    assert items_page_2[0].email == "user2@example.com"


def test_list_users_filters_by_status(db_session):
    seed_users(db_session, 2)
    repo = UserRepository(db_session)

    # mark first user inactive
    first = repo.list_users(page=1, limit=1, status=UserStatus.active)[0][0]
    first.status = UserStatus.inactive
    db_session.commit()

    active_items, total = repo.list_users(page=1, limit=10, status=UserStatus.active)
    assert total == 1
    assert all(item.status == UserStatus.active for item in active_items)

    all_items, total_all = repo.list_users(page=1, limit=10, status="all")
    assert total_all == 2
    assert len(all_items) == 2

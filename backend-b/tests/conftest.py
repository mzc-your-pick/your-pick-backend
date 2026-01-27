import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db


# 테스트용 인메모리 SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db():
    """테스트용 DB 세션"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """테스트용 FastAPI 클라이언트"""
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine)

    with TestClient(app) as c:
        yield c

    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


@pytest.fixture
def sample_poll(db):
    """테스트용 샘플 Poll 데이터"""
    from app.models.poll import Poll
    import json

    poll = Poll(
        id=1,
        matchup_id=1,
        title="A셰프 vs B셰프",
        poll_type="VS",
        options=["A셰프", "B셰프"],
        status="OPEN",
        panel_result={"A셰프": 70, "B셰프": 30},
        result_revealed=False
    )
    db.add(poll)
    db.commit()
    return poll

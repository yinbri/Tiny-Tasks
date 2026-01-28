import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.db import Base, get_db

@pytest.fixture()
def client(tmp_path):
    # 1) make a fresh DB file for this test
    db_file = tmp_path / "test.db"
    test_db_url = f"sqlite:///{db_file}"

    # 2) create a fresh engine + sessionmaker
    engine = create_engine(test_db_url, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # 3) create tables in this fresh DB
    Base.metadata.create_all(bind=engine)

    # 4) override get_db dependency to use the test DB
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    # 5) give the test a client
    with TestClient(app) as c:
        yield c

    # 6) cleanup override
    app.dependency_overrides.clear()

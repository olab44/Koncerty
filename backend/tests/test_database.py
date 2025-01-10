import pytest
from src.database import get_session
from sqlalchemy.orm import Session

def test_get_session():
    session = next(get_session())
    assert isinstance(session, Session)
    session.close()

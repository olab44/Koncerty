# tests/test_database.py
import pytest
from src.database import get_session
from sqlalchemy.orm import Session

def test_get_session():
    session = next(get_session())  # Inicjowanie sesji
    assert isinstance(session, Session)  # Sprawdzamy, czy to obiekt sesji
    session.close()  # Zamykamy sesję po teście

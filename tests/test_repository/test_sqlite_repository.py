from bookkeeper.repository.sqlite_repository import SQLiteRepository

import pytest


@pytest.fixture
def custom_class():
    class Custom():
        pk: int = 0
        f1: int = 10
        f2_name: str = "f2_value"
    return Custom


@pytest.fixture
def repo(custom_class):
    return SQLiteRepository(db_file="database/test_sqlrepo.db", cls=type(custom_class()))

def test_crud(repo, custom_class):
    obj = custom_class()
    pk = repo.add(obj)
    assert obj.pk == pk
    # TODO: test update and delete


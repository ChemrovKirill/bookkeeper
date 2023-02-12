from bookkeeper.repository.sqlite_repository import SQLiteRepository

import pytest


@pytest.fixture
def custom_class():
    class Custom():
        pk: int = 0
        f1: int = 0
        f2_name: str = "f2_value"
    return Custom


@pytest.fixture
def repo(custom_class):
    return SQLiteRepository(db_file="database/test_sqlrepo.db", cls=type(custom_class()))


def test_crud(repo, custom_class):
    # create
    obj_add = custom_class()
    obj_add.f1 = 1
    obj_add.f2_name = "test_crud"
    pk = repo.add(obj_add)
    assert pk == obj_add.pk
    # read
    obj_get = repo.get(pk)
    assert obj_get is not None
    assert obj_get.pk == obj_add.pk
    assert obj_get.f1 == obj_add.f1
    assert obj_get.f2_name == obj_add.f2_name
    # update
    obj_upd = custom_class()
    obj_upd.pk = pk
    obj_upd.f1 = 1
    obj_upd.f2_name = "test_crud_upd"
    repo.update(obj_upd)
    obj_get = repo.get(pk)
    assert obj_get.pk == obj_upd.pk
    assert obj_get.f1 == obj_upd.f1
    assert obj_get.f2_name == obj_upd.f2_name
    # delete
    repo.delete(pk)
    assert repo.get(pk) is None


def test_cannot_add_with_pk(repo, custom_class):
    obj = custom_class()
    obj.pk = 1
    with pytest.raises(ValueError):
        repo.add(obj)


def test_cannot_add_without_pk(repo):
    with pytest.raises(ValueError):
        repo.add(0)


def test_cannot_update_without_pk(repo, custom_class):
    obj = custom_class()
    with pytest.raises(ValueError):
        repo.update(obj)


def test_cannot_update_unexistent(repo, custom_class):
    obj = custom_class()
    obj.pk = -1
    with pytest.raises(ValueError):
        repo.update(obj)


def test_cannot_update_unexistent(repo, custom_class):
    with pytest.raises(ValueError):
        repo.delete(-1)

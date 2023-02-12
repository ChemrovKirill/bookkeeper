from bookkeeper.repository.sqlite_repository import SQLiteRepository

import pytest
import sqlite3

DB_FILE = "database/test_sqlrepo.db"

@pytest.fixture
def create_bd():
    with sqlite3.connect(DB_FILE) as con:
        cur = con.cursor()
        cur.execute(f"DROP TABLE custom")
    with sqlite3.connect(DB_FILE) as con:
        cur = con.cursor()
        cur.execute(f"CREATE TABLE custom(f1, f2)")
    con.close()


@pytest.fixture
def custom_class():
    class Custom():
        pk: int = 0
        f1: int = 0
        f2: str = "f2_value"
    return Custom


@pytest.fixture
def repo(custom_class, create_bd):
    return SQLiteRepository(db_file=DB_FILE, cls=type(custom_class()))


def test_crud(repo, custom_class):
    # create
    obj_add = custom_class()
    obj_add.f1 = 1
    obj_add.f2 = "test_crud"
    pk = repo.add(obj_add)
    assert pk == obj_add.pk
    # read
    obj_get = repo.get(pk)
    assert obj_get is not None
    assert obj_get.pk == obj_add.pk
    assert obj_get.f1 == obj_add.f1
    assert obj_get.f2 == obj_add.f2
    # update
    obj_upd = custom_class()
    obj_upd.pk = pk
    obj_upd.f1 = 11
    obj_upd.f2 = "test_crud_upd"
    repo.update(obj_upd)
    obj_get = repo.get(pk)
    assert obj_get.pk == obj_upd.pk
    assert obj_get.f1 == obj_upd.f1
    assert obj_get.f2 == obj_upd.f2
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


def test_get_all(repo, custom_class):
    objects = [custom_class() for i in range(5)]
    for o in objects:
        repo.add(o)
    objects_pk = [o.pk for o in objects]
    objects_get_pk = [o.pk for o in repo.get_all()]
    assert objects_pk == objects_get_pk

def test_get_all_with_condition(repo, custom_class):
    objects = []
    for i in range(5):
        o = custom_class()
        o.f1 = i
        o.f2 = 'test'
        repo.add(o)
        objects.append(o)
    object_get_pk = [o.pk for o in repo.get_all({'f1': 0})]
    assert object_get_pk[0] == objects[0].pk
    objects_get_pk = [o.pk for o in repo.get_all({'f2': 'test'})]
    assert objects_get_pk == [o.pk for o in objects]
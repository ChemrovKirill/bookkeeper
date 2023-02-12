"""
Модуль описывает репозиторий, работающий в БД SQLite
"""

from bookkeeper.repository.abstract_repository import AbstractRepository, T
from typing import Any
from inspect import get_annotations
import sqlite3

class SQLiteRepository(AbstractRepository[T]):
    
    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk')
        self.obj_cls = cls
        # with sqlite3.connect(self.db_file) as con:
        #     cur = con.cursor()
        #     names = ', '.join(self.fields.keys())
        #     cur.execute(f"CREATE TABLE {self.table_name}({names})")
        #     con.close()
        
    def add(self, obj: T) -> int:
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'trying to add object {obj} with filled `pk` attribute')
        names = ', '.join(self.fields.keys())
        p = ', '.join("?" * len(self.fields))
        values = [getattr(obj, f) for f in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'INSERT INTO {self.table_name} ({names}) VALUES({p})',
                values
            )
            obj.pk = cur.lastrowid
        con.close()
        return obj.pk

    def get(self, pk: int) -> T | None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            res_row = cur.execute(
                f'SELECT * FROM {self.table_name} '
                + f'WHERE ROWID=={pk}'
            ).fetchone()
        con.close()
        if res_row is None:
            return None
        res_obj = self.obj_cls()
        for field, value in zip(self.fields, res_row):
            setattr(res_obj, field, value)
        res_obj.pk = pk
        return res_obj

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        """
        Получить все записи по некоторому условию
        where - условие в виде словаря {'название_поля': значение}
        если условие не задано (по умолчанию), вернуть все записи
        """

    def update(self, obj: T) -> None:
        fields = ", ".join([f"{f}=?" for f in self.fields.keys()])
        values = [getattr(obj, f) for f in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(
                f'UPDATE {self.table_name} SET {fields} '
                + f'WHERE ROWID=={obj.pk}',
                values
            )
            if cur.rowcount == 0:
                raise ValueError('attempt to update object with unknown primary key')
        con.close()

    def delete(self, pk: int) -> None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(
                f'DELETE FROM  {self.table_name} '
                + f'WHERE ROWID=={pk}'
            )
            if cur.rowcount == 0:
                raise ValueError('attempt to delete object with unknown primary key')
        con.close()
    

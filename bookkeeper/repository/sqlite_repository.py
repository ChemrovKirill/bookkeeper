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
        # with sqlite3.connect(self.db_file) as con:
        #     cur = con.cursor()
        #     names = ', '.join(self.fields.keys())
        #     cur.execute(f"CREATE TABLE {self.table_name}({names})")
        #     con.close()
        
    def add(self, obj: T) -> int:
        names = ', '.join(self.fields.keys())
        p = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
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

    def get(self, pk):
        ...

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        """
        Получить все записи по некоторому условию
        where - условие в виде словаря {'название_поля': значение}
        если условие не задано (по умолчанию), вернуть все записи
        """

    def update(self, obj: T) -> None:
        """ Обновить данные об объекте. Объект должен содержать поле pk. """

    def delete(self, pk: int) -> None:
        """ Удалить запись """
    

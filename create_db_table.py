import sqlite3
from inspect import get_annotations
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget

db_file = "database/simple-client-sql.db"
for cls in [Category, Expense, Budget]:
    table_name = cls.__name__.lower()
    fields = get_annotations(cls, eval_str=True)
    fields.pop('pk')
    with sqlite3.connect(db_file) as con:
        cur = con.cursor()
        cur.execute(f"CREATE TABLE {table_name}({', '.join(fields.keys())})")
    con.close()
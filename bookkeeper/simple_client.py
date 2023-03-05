"""
Простой тестовый скрипт для терминала
"""

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.utils import read_tree

cat_repo = MemoryRepository[Category]()
exp_repo = MemoryRepository[Expense]()
budget_repo = MemoryRepository[Budget]()

cats = '''
продукты
    мясо
        сырое мясо
        мясные продукты
    сладости
книги
одежда
'''.splitlines()

Category.create_from_tree(read_tree(cats), cat_repo)

day_budget = Budget(limitation=3000, period="day", spent=0)
budget_repo.add(day_budget)

while True:
    try:
        cmd = input('$> ')
    except EOFError:
        break
    if not cmd:
        continue
    if cmd == 'категории':
        print(*cat_repo.get_all(), sep='\n')
    elif cmd == 'бюджет':
        print(*budget_repo.get_all(), sep='\n')
    elif cmd == 'расходы':
        print(*exp_repo.get_all(), sep='\n')
    elif cmd[0].isdecimal():
        amount, name = cmd.split(maxsplit=1)
        try:
            cat = cat_repo.get_all({'name': name})[0]
        except IndexError:
            print(f'категория {name} не найдена')
            continue
        exp = Expense(int(amount), cat.pk)
        exp_repo.add(exp)
        print(exp)
        for budget in budget_repo.get_all():
            budget.update_spent(exp_repo)

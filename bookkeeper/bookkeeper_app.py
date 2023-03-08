from bookkeeper.view.view import AbstractView, View
from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense

class Bookkeeper:
    
    def __init__(self,
                 view: AbstractView,
                 repository_type: type):
        self.view = view
        self.category_rep = repository_type[Category](
                            db_file="database/bookkeeper.db",
                            cls=Category)
        self.categories = self.category_rep.get_all()
        self.view.set_categories(self.categories)
        #self.view.set_cat_modifier(self.modify_cat)
        self.view.set_cat_adder(self.add_category)
        self.view.set_cat_deleter(self.delete_category)
        self.view.set_cat_checker(self.cat_checker)

        self.expense_rep = repository_type[Expense](
                           db_file="database/bookkeeper.db",
                           cls=Expense)
        self.expenses = self.expense_rep.get_all()
        self.view.set_expenses(self.expenses)
        self.view.set_exp_adder(self.add_expense)

    def start_app(self):
        self.view.show_main_window()
        
    # def modify_cat(self, cat: Category) -> None:
    #     self.category_rep.update(cat)
    #     self.view.set_categories(self.categories)

    def cat_checker(self, cat_name: str):
        if cat_name not in [c.name for c in self.categories]:
            raise ValueError(f'Категории "{cat_name}" не существует')

    def add_category(self, name, parent):
        if name in [c.name for c in self.categories]:
            raise ValueError(f'Категория "{name}" уже существует')
        if parent is not None:
            if parent not in [c.name for c in self.categories]:
                raise ValueError(f'Категории "{parent}" не существует')
            parent_pk = self.category_rep.get_all(where={'name':parent})[0].pk
        else:
            parent_pk = None
        cat = Category(name, parent_pk)
        self.category_rep.add(cat)
        self.categories.append(cat)
        self.view.set_categories(self.categories)

    def delete_category(self, cat_name: str):
        cat = self.category_rep.get_all(where={"name":cat_name})
        if len(cat) == 0:
            raise ValueError(f'Категории "{cat_name}" не существует')
        else:
            cat = cat[0]
        self.category_rep.delete(cat.pk)
        # меняет удаленную категорию на родителя (None если родителя нет)
        for child in self.category_rep.get_all(where={'parent':cat.pk}):
            child.parent = cat.parent
            self.category_rep.update(child)
        self.categories = self.category_rep.get_all()
        self.view.set_categories(self.categories)
        # устанавливает None вместо удаленной категории
        for exp in self.expense_rep.get_all(where={'category':cat.pk}):
            exp.category = None
            self.expense_rep.update(exp)
        self.expenses = self.expense_rep.get_all()
        self.view.set_expenses(self.expenses)     
        
    def add_expense(self, amount: str, cat_name: str):
        amount = int(amount)
        if amount <= 0:
            raise ValueError(f'Удачная покупка! Записывать не буду.')
        cat = self.category_rep.get_all(where={"name":cat_name})
        if len(cat) == 0:
            raise ValueError(f'Категории "{cat_name}" не существует')
        else:
            cat = cat[0]
        new_exp = Expense(amount, cat.pk)
        self.expense_rep.add(new_exp)
        self.expenses = self.expense_rep.get_all()
        self.view.set_expenses(self.expenses)
        


if __name__ == '__main__':
    view = View()
    bookkeeper_app = Bookkeeper(view, SQLiteRepository)
    bookkeeper_app.start_app()


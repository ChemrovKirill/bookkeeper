import sys
from typing import Protocol
from collections.abc import Callable
from PySide6 import QtWidgets

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.view.main_window import MainWindow
from bookkeeper.view.palette_mode import PaletteMode
from bookkeeper.view.budget import BudgetTableGroup
from bookkeeper.view.new_expense import NewExpenseGroup
from bookkeeper.view.expenses import ExpensesTableGroup
from bookkeeper.view.categories_edit import CategoriesEditWindow


class AbstractView(Protocol):

    def show_main_window() -> None:
        pass

    def set_category_list(cats : list[Category]) -> None:
        pass
    
    def set_cat_modifier(handler: Callable[[Category], None]):
        pass


def handle_error(widget, handler):
    def inner(*args, **kwargs):
        try:
            handler(*args, **kwargs)
        except ValueError as ex:
            QtWidgets.QMessageBox.critical(widget, 'Ошибка', str(ex))
    return inner


class View:

    categories: list[Category] = []
    main_window: MainWindow
    budget_table: BudgetTableGroup
    new_expense: NewExpenseGroup
    expenses_table: ExpensesTableGroup
    cats_edit_window: CategoriesEditWindow

    def __init__(self):
        self.config_app()
        self.config_cats_edit()
        self.budget_table = BudgetTableGroup()
        self.new_expense = NewExpenseGroup(self.categories, 
                                           self.cats_edit_show,
                                           self.add_expense)
        self.expenses_table = ExpensesTableGroup(self.catpk_to_name)
        self.config_main_window()
        

    def show_main_window(self):
        self.main_window.show()
        print("run app")
        print(f"Application ends with exit status {self.app.exec()}")
        sys.exit()
    
    def config_app(self):
        self.app = QtWidgets.QApplication(sys.argv)
        #self.app.setQuitOnLastWindowClosed(False)
        self.app.setStyle("Fusion")
        self.app.setPalette(PaletteMode(is_dark_mode=True))

    def config_main_window(self):
        self.main_window = MainWindow(self.budget_table, 
                                      self.new_expense, 
                                      self.expenses_table)
        self.main_window.resize(1000, 800)

    def config_cats_edit(self):
        self.cats_edit_window = CategoriesEditWindow(self.categories, 
                                                     self.add_category,
                                                     self.delete_category)
        self.cats_edit_window.setWindowTitle("Редактирование категорий")
        self.cats_edit_window.resize(600, 600)

    def cats_edit_show(self):
        #self.config_cats_edit()
        self.cats_edit_window.show()

    def set_categories(self, cats: list[Category]) -> None:
        self.categories = cats
        self.new_expense.set_categories(self.categories)
        self.cats_edit_window.set_categories(self.categories)

    def catpk_to_name(self, pk: int) -> str:
        name = [c.name for c in self.categories if int(c.pk) == int(pk)]
        if len(name):
            return str(name[0])
        return ""

    # def set_cat_modifier(self, handler: Callable[[Category], None]):
    #     pass

    def set_cat_adder(self, handler):
        """ устанавливает метод добавления категории (из bookkeeper_app)"""
        self.cat_adder = handle_error(self.main_window, handler)

    def set_cat_deleter(self, handler):
        """ устанавливает метод удаления категории (из bookkeeper_app)"""
        self.cat_deleter = handle_error(self.main_window, handler)

    def set_cat_checker(self, handler):
        """ устанавливает метод проверки существования категории (из bookkeeper_app)"""
        self.cat_checker = handle_error(self.main_window, handler)
        self.cats_edit_window.set_cat_checker(self.cat_checker)

    def add_category(self, name, parent):
        self.cat_adder(name, parent)
        # try:
        #     self.cat_adder(name, parent)
        # except ValidationError as ex:
        #     QMessageBox.critical(self, 'Ошибка', str(ex))

    def delete_category(self, cat_name: str):
        self.cat_deleter(cat_name)
        # del_subcats, del_expenses = self.ask_del_cat()
        # self.cat_deleter(cat, del_subcats, del_expenses)

    def set_expenses(self, exps: list[Expense]) -> None:
        self.expenses = exps
        self.expenses_table.set_expenses(self.expenses)

    def set_exp_adder(self, handler):
        """ устанавливает метод добавления траты (из bookkeeper_app)"""
        self.exp_adder = handle_error(self.main_window, handler)

    def add_expense(self, amount: str, cat_name: str, comment: str = ""):
        self.exp_adder(amount, cat_name, comment)
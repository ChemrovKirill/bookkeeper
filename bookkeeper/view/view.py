import sys
from typing import Protocol
from collections.abc import Callable
from PySide6 import QtWidgets

from bookkeeper.models.category import Category
from bookkeeper.view.main_window import MainWindow
from bookkeeper.view.palette_mode import PaletteMode

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
        except ValidationError as ex:
            QMessageBox.critical(self, 'Ошибка', str(ex))
        return inner


class View:

    categories: list[Category] = []

    def __init__(self):
        self.config_app()
        self.config_main_window()

    def show_main_window(self):
        self.window.show()
        sys.exit(self.app.exec())
    
    def config_app(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.app.setStyle("Fusion")
        self.app.setPalette(PaletteMode(is_dark_mode=True))

    def config_main_window(self):
        self.window = MainWindow(cats=self.categories)
        self.window.resize(800, 800)

    def set_categories(self, cats: list[Category]) -> None:
        self.categories = cats
        self.window.set_categories(cats)
    
    def set_cat_modifier(self, handler: Callable[[Category], None]):
        pass

    def set_cat_adder(self, handler):
        self.cat_adder = handle_error(self, handler)

    
    def add_category(self):
        # получение данных из формочки
        name = ...
        parent = ...
        try:
            self.cat_adder(name, parent)
        except ValidationError as ex:
            QMessageBox.critical(self, 'Ошибка', str(ex))

    def delete_category(self):
        cat = ... # определить выбранную категорию
        del_subcats, del_expenses = self.ask_del_cat()
        self.cat_deleter(cat, del_subcats, del_expenses)
from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

from bookkeeper.view.budget import BudgetTableGroup
from bookkeeper.view.new_expense import NewExpenseGroup
from bookkeeper.view.expenses import ExpensesTableGroup
from bookkeeper.view.group_widgets import LabeledCheckBox
from bookkeeper.view.palette_mode import PaletteMode
from bookkeeper.models.category import Category
from bookkeeper.view.categories_edit import CategoriesEditWindow


class MainWindow(QtWidgets.QWidget):
    def __init__(self, cats: list[Category], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.categories = cats
        self.vbox = QtWidgets.QVBoxLayout()
        self.setWindowTitle("Bookkeeper v0.2")
        self.theme = LabeledCheckBox("Темная тема", 
                                     init_state=Qt.Checked, 
                                     chstate_func=self.change_theme)
        self.vbox.addWidget(self.theme, stretch=0.1, alignment=Qt.AlignRight)
        # Бюджет
        self.budget_table = BudgetTableGroup()
        self.vbox.addWidget(self.budget_table, stretch=3)
        # Новая трата
        self.new_expense = NewExpenseGroup(self.categories, self.cats_edit)
        self.vbox.addWidget(self.new_expense, stretch=1)
        # Расходы
        self.expenses_table = ExpensesTableGroup()
        self.vbox.addWidget(self.expenses_table, stretch=6)
        self.setLayout(self.vbox)

    def set_categories(self, cats: list[Category]) -> None:
        self.categories = cats
        self.new_expense.set_categories(self.categories)

    def cats_edit(self):
        self.window = CategoriesEditWindow(self.categories)
        self.window.setWindowTitle("Редактирование категорий")
        self.window.resize(600, 600)
        self.window.show()

    def change_theme(self, status):
        app = QtWidgets.QApplication.instance()
        if(self.theme.check_box.isChecked()):
            app.setPalette(PaletteMode(is_dark_mode=True))
        else:
            app.setPalette(PaletteMode(is_dark_mode=False))

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Закрыть приложение',
        "Вы уверены?\nВсе несохраненные данные будут потеряны.")
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

# class MainWindow(QtWidgets.QMainWindow):
#     def __init__(self, *arg):
#         super().__init__()
#         self.setWindowTitle("Bookkeeper v0.1")
#         self.main_widget = MainWidget()
#         self.setCentralWidget(self.main_widget)

#         # toolbar = QtWidgets.QToolBar("My main toolbar")
#         # button_action = QAction("toolBar", self)
#         # button_action.triggered.connect(lambda s: print(s))
#         # toolbar.addAction(button_action)
#         # self.addToolBar(toolbar)

#         #menu = self.menuBar().addMenu("menuBar")
#         # menu.addAction(button_action)

#         self.setStatusBar(QtWidgets.QStatusBar(self))
#         self.statusBar().setStatusTip("bookkeeper v0.1")



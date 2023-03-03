import sys
from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor, QAction

from bookkeeper.view.budget import BudgetTableGroup
from bookkeeper.view.new_expense import NewExpenseGroup
from bookkeeper.view.expenses import ExpensesTableGroup
from bookkeeper.view.group_widgets import LabeledCheckBox


class PaletteMode(QPalette):
    def __init__(self, is_dark_mode=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if is_dark_mode:
            self.setColor(QPalette.Window, QColor(53, 53, 53))
            self.setColor(QPalette.WindowText, Qt.white)
            self.setColor(QPalette.Base, QColor(25, 25, 25))
            self.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            self.setColor(QPalette.ToolTipBase, Qt.black)
            self.setColor(QPalette.ToolTipText, Qt.white)
            self.setColor(QPalette.Text, Qt.white)
            self.setColor(QPalette.Button, QColor(53, 53, 53))
            self.setColor(QPalette.ButtonText, Qt.white)
            self.setColor(QPalette.BrightText, Qt.red)
            self.setColor(QPalette.Link, QColor(42, 130, 218))
            self.setColor(QPalette.Highlight, QColor(42, 130, 218))
            self.setColor(QPalette.HighlightedText, Qt.black)


class MainWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vbox = QtWidgets.QVBoxLayout()
        self.theme = LabeledCheckBox("Темная тема", 
                                     init_state=Qt.Checked, 
                                     chstate_func=self.change_theme)
        self.vbox.addWidget(self.theme, stretch=0.1, alignment=Qt.AlignRight)
        # Бюджет
        self.budget_table = BudgetTableGroup()
        self.vbox.addWidget(self.budget_table, stretch=3)
        # Новая трата
        self.new_expense = NewExpenseGroup()
        self.vbox.addWidget(self.new_expense, stretch=1)
        # Расходы
        self.expenses_table = ExpensesTableGroup()
        self.vbox.addWidget(self.expenses_table, stretch=6)
        self.setLayout(self.vbox)

    def change_theme(self, status):
        app = QtWidgets.QApplication.instance()
        if(self.theme.check_box.isChecked()):
            app.setPalette(PaletteMode(is_dark_mode=True))
        else:
            app.setPalette(PaletteMode(is_dark_mode=False))


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *arg):
        super().__init__()
        self.setWindowTitle("Bookkeeper v0.1")
        self.main_widget = MainWidget()
        self.setCentralWidget(self.main_widget)

        # toolbar = QtWidgets.QToolBar("My main toolbar")
        # button_action = QAction("toolBar", self)
        # button_action.triggered.connect(lambda s: print(s))
        # toolbar.addAction(button_action)
        # self.addToolBar(toolbar)

        #menu = self.menuBar().addMenu("menuBar")
        # menu.addAction(button_action)

        self.setStatusBar(QtWidgets.QStatusBar(self))
        self.statusBar().setStatusTip("bookkeeper v0.1")

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Закрыть приложение',
        "Вы уверены?\nВсе несохраненные данные будут потеряны.")
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setPalette(PaletteMode(is_dark_mode=True))

    window = MainWindow()
    window.resize(800, 800)
    window.show()
    sys.exit(app.exec())

    # import sys
    # from PySide6 import QtWidgets
    # app = QtWidgets.QApplication(sys.argv)
    # window = QtWidgets.QWidget()
    # window.show()
    # sys.exit(app.exec())

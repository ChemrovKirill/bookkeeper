from PySide6 import QtWidgets

from bookkeeper.view.group_widgets import GroupLabel
from bookkeeper.models.expense import Expense


class ExpensesTableWidget(QtWidgets.QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setColumnCount(4)
        self.setRowCount(20)
        self.headers = "Дата Сумма Категория Комментарий".split()
        self.setHorizontalHeaderLabels(self.headers)
        header = self.horizontalHeader()
        header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(
            3, QtWidgets.QHeaderView.Stretch)
        self.setEditTriggers(
            QtWidgets.QAbstractItemView.DoubleClicked)
        self.verticalHeader().hide()

    def add_data(self, data: list[list[str]]):
        for i, row in enumerate(data):
            for j, x in enumerate(row):
                self.setItem(
                    i, j,
                    QtWidgets.QTableWidgetItem(x.capitalize())
                )

class ExpensesTableGroup(QtWidgets.QGroupBox):
    def __init__(self, catpk_to_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.catpk_to_name = catpk_to_name
        self.vbox = QtWidgets.QVBoxLayout()
        self.label = GroupLabel("<b>Последние траты</b>")
        self.vbox.addWidget(self.label)
        self.table = ExpensesTableWidget()
        #self.table.add_data(self.data)
        self.vbox.addWidget(self.table)
        self.setLayout(self.vbox)

    def set_expenses(self, exps: list[Expense]):
        self.expenses = exps
        self.exps_to_data(self.expenses)
        self.table.clearContents()
        self.table.add_data(self.data)

    def exps_to_data(self, exps: list[Expense]):
        self.data = []
        for exp in exps:
            data_item = ["","","",""]
            if exp.expense_date:
                data_item[0] = str(exp.expense_date)
            if exp.amount:
                data_item[1] = str(exp.amount)
            if exp.category:
                data_item[2] = str(
                    self.catpk_to_name(exp.category))
            if exp.comment:
                data_item[3] = str(exp.comment)
            self.data.append(data_item)
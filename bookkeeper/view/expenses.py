from PySide6 import QtWidgets

from bookkeeper.view.group_widgets import GroupLabel


class ExpensesTableWidget(QtWidgets.QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setColumnCount(4)
        self.setRowCount(20)
        headers = "Дата Сумма Категория Комментарий".split()
        self.setHorizontalHeaderLabels(headers)
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
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.verticalHeader().hide()

    def add_data(self, data: list[list[str]]):
        for i, row in enumerate(data):
            for j, x in enumerate(row):
                self.setItem(
                    i, j,
                    QtWidgets.QTableWidgetItem(x.capitalize())
                )

class ExpensesTableGroup(QtWidgets.QGroupBox):
    data = [["2023-26-02 14:30:00", str(100), "кофе", ""],
            ["2023-26-02 14:00:00", str(1000), "одежда", ""],
            ["2023-25-02 18:30:00", str(500), "мясо", ""],
            ["2023-20-02 19:46:00", str(33), "вода", ""],]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vbox = QtWidgets.QVBoxLayout()
        self.label = GroupLabel("<b>Последние траты</b>")
        self.vbox.addWidget(self.label)
        self.table = ExpensesTableWidget()
        self.table.add_data(self.data)
        self.vbox.addWidget(self.table)
        self.setLayout(self.vbox)
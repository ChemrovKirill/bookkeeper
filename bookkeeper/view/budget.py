from PySide6 import QtWidgets

from bookkeeper.view.group_widgets import GroupLabel


class BudgetTableWidget(QtWidgets.QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setColumnCount(3)
        self.setRowCount(3)
        hheaders = "Бюджет Потрачено Остаток".split()
        self.setHorizontalHeaderLabels(hheaders)
        vheaders = "День Неделя Месяц".split()
        self.setVerticalHeaderLabels(vheaders)
        for h in [self.horizontalHeader(), self.verticalHeader(),]:
            h.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)     
        self.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)

    def add_data(self, data: list[list[str]]):
        for i, row in enumerate(data):
            for j, x in enumerate(row):
                self.setItem(
                    i, j,
                    QtWidgets.QTableWidgetItem(x.capitalize())
                )

class BudgetTableGroup(QtWidgets.QGroupBox):
    data = [['1000', '999', '1'],
            ['7000', '6999', '1'],
            ['30000', '29999', '1'],]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vbox = QtWidgets.QVBoxLayout()
        self.label = GroupLabel("<b>Бюджет</b>")
        self.vbox.addWidget(self.label)
        self.table = BudgetTableWidget()
        self.table.add_data(self.data)
        self.vbox.addWidget(self.table)
        self.setLayout(self.vbox)
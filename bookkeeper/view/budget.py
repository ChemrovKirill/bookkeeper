""" Модуль описывает группу с таблицей бюджетов """
# pylint: disable = no-name-in-module
# pylint: disable=c-extension-no-member
# mypy: disable-error-code="attr-defined"
from PySide6 import QtWidgets
from PySide6.QtCore import Qt

from bookkeeper.view.group_widgets import GroupLabel
from bookkeeper.models.budget import Budget


class BudgetTableWidget(QtWidgets.QTableWidget):
    """ Виджет-таблица бюджетов """

    def __init__(self, bdg_modifier, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = []
        self.bdg_modifier = bdg_modifier
        self.setColumnCount(3)
        self.setRowCount(3)
        self.row_to_period = {0: "day", 1: "week", 2: "month"}
        hheaders = "Бюджет Потрачено Остаток".split()
        self.setHorizontalHeaderLabels(hheaders)
        vheaders = "День Неделя Месяц".split()
        self.setVerticalHeaderLabels(vheaders)
        for hdr in [self.horizontalHeader(), self.verticalHeader(),]:
            hdr.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.setEditTriggers(
            QtWidgets.QAbstractItemView.DoubleClicked)
        self.cellDoubleClicked.connect(self.double_click)

    # pylint: disable=unused-argument
    # pylint: disable=duplicate-code
    def double_click(self, row, columns) -> None:
        """ Обрабатывает двойное нажатие по ячейке """
        self.cellChanged.connect(self.cell_changed)

    def cell_changed(self, row, column) -> None:
        """ Обрабатывает изменение ячейки """
        self.cellChanged.disconnect(self.cell_changed)
        pk = self.data[row][-1]
        new_limit = self.item(row, column).text()
        self.bdg_modifier(pk, new_limit, self.row_to_period[row])

    # pylint: disable=duplicate-code
    def add_data(self, data: list[list[str]]) -> None:
        """ Добавляет данные в таблицу """
        self.data = data
        for i_row, row in enumerate(data):
            for j_col, text in enumerate(row[:-1]):
                self.setItem(
                    i_row, j_col,
                    QtWidgets.QTableWidgetItem(text.capitalize())
                )
                self.item(i_row, j_col).setTextAlignment(Qt.AlignCenter)
                if j_col == 0:
                    self.item(i_row, j_col).setFlags(Qt.ItemIsEditable
                                                     | Qt.ItemIsEnabled
                                                     | Qt.ItemIsSelectable)
                else:
                    self.item(i_row, j_col).setFlags(Qt.ItemIsEnabled)


class BudgetTableGroup(QtWidgets.QGroupBox):
    """ Группа бюджетов с таблицей и заголовком"""

    def __init__(self, bdg_modifier, *args, **kwargs):
        self.data = []
        self.budgets = []
        super().__init__(*args, **kwargs)
        self.vbox = QtWidgets.QVBoxLayout()
        self.label = GroupLabel("<b>Бюджет</b>")
        self.vbox.addWidget(self.label)
        self.table = BudgetTableWidget(bdg_modifier)
        self.vbox.addWidget(self.table)
        self.setLayout(self.vbox)

    def set_budgets(self, budgets: list[Budget]) -> None:
        """ Устанавлиявает список бюджетов """
        self.budgets = budgets
        self.data = self.budgets_to_data(self.budgets)
        self.table.clearContents()
        self.table.add_data(self.data)

    def budgets_to_data(self, budgets: list[Budget]) -> list[list[str]]:
        """ Конвертирует объекты бюджетов в данные для таблицы """
        data = []
        for period in ["day", "week", "month"]:
            bdg = [bi for bi in budgets if bi.period == period]
            if len(bdg) == 0:
                data.append(["- Не установлен -", "", "", None])
            else:
                bdg = bdg[0]
                data.append([str(bdg.limitation), str(bdg.spent),
                            str(int(bdg.limitation) - int(bdg.spent)), bdg.pk])
        return data

"""
Тесты GUI для модуля с таблицей расходов
"""
import pytest
from pytestqt.qt_compat import qt_api

from bookkeeper.view.expenses import ExpensesTableWidget, ExpensesTableGroup

def exp_modifier(pk, attr, new_val):
    pass

def test_create_widget(qtbot):
    widget = ExpensesTableWidget(exp_modifier)
    qtbot.addWidget(widget)

def test_add_data(qtbot):
    widget = ExpensesTableWidget(exp_modifier)
    qtbot.addWidget(widget)
    test_data = [["1_1","1_2","1_3","1_4",1],
                 ["2_1","2_2","2_3","2_4",2],]
    widget.add_data(test_data)
    assert widget.data == test_data
    for i, row in enumerate(test_data):
        for j, x in enumerate(row[:-1]):
            assert widget.item(i, j).text() == test_data[i][j]

def test_cell_select(qtbot):
    widget = ExpensesTableWidget(exp_modifier)
    qtbot.addWidget(widget)
    widget.show()
    qtbot.mouseClick(
        widget.item(1,1),
        qt_api.QtCore.Qt.MouseButton.LeftButton
        )
    qtbot.stop()
    assert widget.selectedItems()[0] == widget.item(1,1)

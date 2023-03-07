from PySide6 import QtWidgets

from bookkeeper.view.group_widgets import GroupLabel, LabeledComboBoxInput, LabeledLineInput
from bookkeeper.models.category import Category

class NewExpenseGroup(QtWidgets.QGroupBox):
    def __init__(self, cats: list[Category], cats_edit_show, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.categories = cats
        self.cats_edit_show = cats_edit_show
        self.cat_names = [c.name for c in cats]
        self.grid = QtWidgets.QGridLayout()
        self.label = GroupLabel("<b>Новая трата</b>")
        self.grid.addWidget(self.label,0,0,1,3)
        self.amount_input = LabeledLineInput("Сумма", "0")
        self.grid.addWidget(self.amount_input,1,0,1,2)
        self.category_input = LabeledComboBoxInput("Категория", self.cat_names)
        self.grid.addWidget(self.category_input,2,0,1,2)
        self.cats_edit_button = QtWidgets.QPushButton('Редактировать')
        self.cats_edit_button.clicked.connect(self.cats_edit_show)
        self.grid.addWidget(self.cats_edit_button,2,2,1,1)
        self.submit_button = QtWidgets.QPushButton('Добавить')
        self.submit_button.clicked.connect(self.submit)
        self.grid.addWidget(self.submit_button,3,0,1,2)
        self.setLayout(self.grid)
    
    def set_categories(self, cats: list[Category]):
        self.categories = cats
        self.cat_names = [c.name for c in cats]
        self.category_input.set_items(self.cat_names)

    def submit(self):
        print(f"Новая трата в категории {self.category_input.text()} на сумму {self.amount_input.text()} добавлена")
        self.amount_input.clear()
        self.category_input.clear()

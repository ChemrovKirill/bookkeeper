from PySide6 import QtWidgets

from bookkeeper.view.group_widgets import GroupLabel, LabeledComboBoxInput, LabeledLineInput
from bookkeeper.view.categories_edit import CategoriesEditWindow

class NewExpenseGroup(QtWidgets.QGroupBox):
    categories = [f"Категория {2*i}" for i in range(11)]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid = QtWidgets.QGridLayout()
        self.label = GroupLabel("<b>Новая трата</b>")
        self.grid.addWidget(self.label,0,0,1,3)
        self.amount_input = LabeledLineInput("Сумма", "0")
        self.grid.addWidget(self.amount_input,1,0,1,2)
        self.category_input = LabeledComboBoxInput("Категория", self.categories)
        self.grid.addWidget(self.category_input,2,0,1,2)
        self.cats_edit_button = QtWidgets.QPushButton('Редактировать')
        self.cats_edit_button.clicked.connect(self.cats_edit)
        self.grid.addWidget(self.cats_edit_button,2,2,1,1)
        self.submit_button = QtWidgets.QPushButton('Добавить')
        self.submit_button.clicked.connect(self.submit)
        self.grid.addWidget(self.submit_button,3,0,1,2)
        self.setLayout(self.grid)
    
    def submit(self):
        print(f"Новая трата в категории {self.category_input.text()} на сумму {self.amount_input.text()} добавлена")
        self.amount_input.clear()
        self.category_input.clear()
    
    def cats_edit(self):
        self.window = CategoriesEditWindow()
        self.window.setWindowTitle("Редактирование категорий")
        self.window.resize(600, 600)
        self.window.show()

from PySide6 import QtWidgets

from bookkeeper.view.group_widgets import GroupLabel, LabeledComboBoxInput, LabeledLineInput
# vvv temp vvv
from bookkeeper.utils import read_tree
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.models.category import Category

cats = '''
продукты
    мясо
        сырое мясо
        мясные продукты
    сладости
книги
одежда
'''.splitlines()

#todo: new file
class CatsEditWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vbox = QtWidgets.QVBoxLayout()
        self.label = GroupLabel("<b>Список категорий</b>")
        self.vbox.addWidget(self.label)
        self.cats_tree = QtWidgets.QTreeWidget()
        self.cats_tree.setColumnCount(1)
        self.cat_repo = MemoryRepository[Category]()
        Category.create_from_tree(read_tree(cats), self.cat_repo)
        top_items = self.find_children()
        self.cats_tree.insertTopLevelItems(0, top_items)
        self.vbox.addWidget(self.cats_tree)
        self.setLayout(self.vbox)
    
    def find_children(self, parent_pk=None):
        items = []
        children = self.cat_repo.get_all(where={'parent':parent_pk})
        for child in children:
            item = QtWidgets.QTreeWidgetItem([child.name])
            item.addChildren(self.find_children(parent_pk=child.pk))
            items.append(item)
        return items
        

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
        self.window = CatsEditWindow()
        self.window.resize(400, 400)
        self.window.show()
        # todo: QTreeWidget

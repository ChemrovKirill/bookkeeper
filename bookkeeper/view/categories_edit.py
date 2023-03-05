
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

class CategoriesEditWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid = QtWidgets.QGridLayout()
        self.label = GroupLabel("<b>Список категорий</b>")
        self.grid.addWidget(self.label, 0, 0, 1, 2)
        self.cats_tree = QtWidgets.QTreeWidget()
        self.cats_tree.setColumnCount(1)
        self.cat_repo = MemoryRepository[Category]()
        Category.create_from_tree(read_tree(cats), self.cat_repo)
        top_items = self.find_children()
        self.cats_tree.insertTopLevelItems(0, top_items)
        self.grid.addWidget(self.cats_tree, 1, 0, 1, 2)
        self.label = GroupLabel("<b>Удаление категории</b>")
        self.grid.addWidget(self.label, 2, 0, 1, 2)
        categories = [cat.name for cat in self.cat_repo.get_all()]
        self.cat_del = LabeledComboBoxInput("Категория", categories)
        self.grid.addWidget(self.cat_del, 3, 0, 1, 1)
        self.cat_del_button = QtWidgets.QPushButton('Удалить')
        self.cat_del_button.clicked.connect(self.cat_del_func)
        self.grid.addWidget(self.cat_del_button, 3, 1, 1, 1)
        self.label = GroupLabel("<b>Добавление категории</b>")
        self.grid.addWidget(self.label, 4, 0, 1, 2)
        categories = [cat.name for cat in self.cat_repo.get_all()]
        self.cat_add_parent = LabeledComboBoxInput("Родитель", 
                                            categories + ["Без родительской категории"])
        self.grid.addWidget(self.cat_add_parent, 5, 0, 1, 1)
        self.cat_add_name = LabeledLineInput("Название", "Новая категория")
        self.grid.addWidget(self.cat_add_name, 6, 0, 1, 1)
        self.cat_add_button = QtWidgets.QPushButton('Добавить')
        self.cat_add_button.clicked.connect(self.cat_add_func)
        self.grid.addWidget(self.cat_add_button, 6, 1, 1, 1)
        self.setLayout(self.grid)

    def cat_del_func(self):
        print(f"Категория {self.cat_del.text()} удалена")
        self.cat_del.clear()
        # todo: upd cat tree view

    def cat_add_func(self):
        if self.cat_add_parent.text() == "Без родительской категории":
            print(f"Категория '{self.cat_add_name.text()}' добавлена")
        else:
            print(f"Подкатегория '{self.cat_add_name.text()}' категории" 
                  + f"'{self.cat_add_parent.text()}' добавлена")
        self.cat_add_name.clear()
        self.cat_add_parent.clear()
        # todo: upd cat tree view
    
    def find_children(self, parent_pk=None):
        items = []
        children = self.cat_repo.get_all(where={'parent':parent_pk})
        for child in children:
            item = QtWidgets.QTreeWidgetItem([child.name])
            item.addChildren(self.find_children(parent_pk=child.pk))
            items.append(item)
        return items
        
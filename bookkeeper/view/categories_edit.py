
from PySide6 import QtWidgets

from bookkeeper.view.group_widgets import GroupLabel, LabeledComboBoxInput, LabeledLineInput

# vvv temp vvv
from bookkeeper.models.category import Category


class CategoriesEditWindow(QtWidgets.QWidget):
    def __init__(self, cats: list[Category],
                 cat_adder, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid = QtWidgets.QGridLayout()
        self.label = GroupLabel("<b>Список категорий</b>")
        self.grid.addWidget(self.label, 0, 0, 1, 2)
        self.cats_tree = QtWidgets.QTreeWidget()
        self.cats_tree.setHeaderLabel("")
        self.grid.addWidget(self.cats_tree, 1, 0, 1, 2)
        self.label = GroupLabel("<b>Удаление категории</b>")
        self.grid.addWidget(self.label, 2, 0, 1, 2)
        self.cat_del = LabeledComboBoxInput("Категория", [])
        self.grid.addWidget(self.cat_del, 3, 0, 1, 1)
        self.cat_del_button = QtWidgets.QPushButton('Удалить')
        self.cat_del_button.clicked.connect(self.cat_del_func)
        self.grid.addWidget(self.cat_del_button, 3, 1, 1, 1)
        self.label = GroupLabel("<b>Добавление категории</b>")
        self.grid.addWidget(self.label, 4, 0, 1, 2)
        self.cat_add_parent = LabeledComboBoxInput("Родитель", [])
        self.grid.addWidget(self.cat_add_parent, 5, 0, 1, 1)
        self.cat_add_name = LabeledLineInput("Название", "Новая категория")
        self.grid.addWidget(self.cat_add_name, 6, 0, 1, 1)
        self.cat_add_button = QtWidgets.QPushButton('Добавить')
        self.cat_add_button.clicked.connect(self.add_category)
        self.grid.addWidget(self.cat_add_button, 6, 1, 1, 1)
        self.setLayout(self.grid)
        self.cat_adder = cat_adder
        self.set_categories(cats)

    def set_categories(self, cats: list[Category]):
        self.categories = cats
        self.cat_names = [c.name for c in cats]
        top_items = self.find_children()
        self.cats_tree.clear()
        self.cats_tree.insertTopLevelItems(0, top_items)
        self.cat_del.set_items(self.cat_names)
        self.cat_add_parent.set_items(self.cat_names
                                      + ["Без родительской категории"])

    def cat_del_func(self):
        print(f"Категория {self.cat_del.text()} удалена")
        self.cat_del.clear()
        # todo: upd cat tree view

    def add_category(self):
        if self.cat_add_parent.text() == "Без родительской категории":
            self.cat_adder(self.cat_add_name.text(), None)
            #print(f"Категория '{self.cat_add_name.text()}' добавлена")
        else:
            self.cat_adder(self.cat_add_name.text(), self.cat_add_parent.text())
            # print(f"Подкатегория '{self.cat_add_name.text()}' категории" 
            #       + f"'{self.cat_add_parent.text()}' добавлена")
        self.cat_add_name.clear()
        self.cat_add_parent.clear()
        # todo: upd cat tree view
    
    def find_children(self, parent_pk=None):
        items = []
        children = [c for c in self.categories if c.parent == parent_pk]
        for child in children:
            item = QtWidgets.QTreeWidgetItem([child.name])
            item.addChildren(self.find_children(parent_pk=child.pk))
            items.append(item)
        return items
        
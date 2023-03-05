from bookkeeper.view.view import AbstractView, View
from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.models.category import Category

class Bookkeeper:
    
    def __init__(self,
                 view: AbstractView,
                 repository_type: type):
        self.view = view
        self.category_rep = repository_type[Category](
                            db_file="database/bookkeeper.db",
                            cls=Category)
        self.categories = self.category_rep.get_all()
        self.view.set_categories(self.categories)
        #self.view.set_cat_modifier(self.modify_cat)

    def start_app(self):
        self.view.show_main_window()
        
    def modify_cat(self, cat: Category) -> None:
        self.category_rep.update(cat)
        self.view.set_categories(self.categories)

    def add_category(self, name, parent):
        if name in [c.name for c in self.categories]:
            raise ValidationError(f'Категория {name} уже существует')
        cat = Category(name, parent)
        self.category_repository.add(cat)
        self.cats.append(cat)
        self.view.set_categories(self.categories)


if __name__ == '__main__':
    view = View()
    bookkeeper_app = Bookkeeper(view, SQLiteRepository)
    bookkeeper_app.start_app()


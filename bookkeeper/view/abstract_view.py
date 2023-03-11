from typing import Protocol
from collections.abc import Callable

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget

class AbstractView(Protocol):

    def show_main_window() -> None:
        pass

    def set_categories(cats : list[Category]) -> None:
        pass

    def set_expenses(cats : list[Expense]) -> None:
        pass

    def set_budgets(cats : list[Budget]) -> None:
        pass
    
    def set_cat_adder(handler: Callable[[str, str], None]) -> None:
        pass

    def set_cat_deleter(handler: Callable[[str], None]) -> None:
        pass

    def set_cat_checker(handler: Callable[[str], None]) -> None:
        pass

    def set_bdg_modifier(handler: Callable[['int | None', str, str], 
                                                        None]) -> None:
        pass

    def set_exp_adder(handler: Callable[[str, str, str], None]) -> None:
        pass

    def set_exp_deleter(handler: Callable[[list[int]], None]) -> None:
        pass

    def set_exp_modifier(handler: Callable[[int, str, str], None]) -> None:
        pass

    def death() -> None:
        pass

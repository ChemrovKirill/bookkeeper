from typing import Protocol
from collections.abc import Callable

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget

class AbstractView(Protocol):

    def set_categories(cats : list[Category]) -> None:
        """ устанавливает список категорий """

    def set_expenses(cats : list[Expense]) -> None:
        """ устанавливает список трат """

    def set_budgets(cats : list[Budget]) -> None:
        """ устанавливает список бюджетов """
    
    def set_cat_adder(handler: Callable[[str, str], None]) -> None:
        """ устанавливает функцию добавления категории """

    def set_cat_deleter(handler: Callable[[str], None]) -> None:
        """ устанавливает функцию удаления категории """

    def set_cat_checker(handler: Callable[[str], None]) -> None:
        """ устанавливает функцию проверки названия категории """

    def set_bdg_modifier(handler: Callable[['int | None', str, str], 
                                                        None]) -> None:
        """ 
        устанавливает функцию изменения (удаления, добавления) бюджета
        """

    def set_exp_adder(handler: Callable[[str, str, str], None]) -> None:
        """ устанавливает функцию добавления траты """

    def set_exp_deleter(handler: Callable[[list[int]], None]) -> None:
        """ устанавливает функцию удаления траты """

    def set_exp_modifier(handler: Callable[[int, str, str], None]) -> None:
        """ устанавливает функцию изменения траты """

    def death() -> None:
        """ устанавливает функцию превышения бюджета """

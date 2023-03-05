"""
Модель бюджета
"""
from dataclasses import dataclass
from datetime import datetime

from ..repository.abstract_repository import AbstractRepository
from bookkeeper.models.expense import Expense


@dataclass
class Budget:
    """
    Бюджет, хранит название периода в атрибуте period, 
    допустимую сумму трат за период в атрибуте limitation,
    потраченную за период сумму в атрибуте spent
    """
    limitation: int
    period: str
    spent: str = 0
    pk: str = 0

    def __init__(self, limitation: int, period: str, 
                       spent: str = 0, pk: str = 0):
        if period not in ["day"]:
            raise ValueError(f'unknown period "{period}" for budget'
            + 'should be "day" or ')
        self.limitation = limitation
        self.period = period
        self.spent = spent
        self.pk = pk

    def set_limit(self, limitation: int) -> None:
        self.limitation = limitation

    def update_spent(self, exp_repo: AbstractRepository[Expense]) -> None:
        if self.period.lower() == "day":
            date = datetime.now().isoformat()[:10]
            period_exps = exp_repo.get_all(where={"expense_date":f"{date}%"})
        self.spent = sum([exp.amount for exp in period_exps])
    
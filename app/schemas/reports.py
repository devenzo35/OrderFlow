from pydantic import BaseModel


class MonthlyBalance(BaseModel):
    month: str
    expense: float


class CategoryDistribution(BaseModel):
    category: str
    total: float


class investment_evolution(BaseModel):
    pass


class custom(BaseModel):
    pass

from pydantic import BaseModel

class Expense(BaseModel):
    title: str
    amount: float
    category: str


expense = Expense(
    title="Movie",
    amount=150,
    category="entertainment"
)

print(expense)
print(type(expense))

print(expense.title)
print(expense.amount)
print(expense.category)

print(expense.model_dump())
print(type(expense.model_dump()))


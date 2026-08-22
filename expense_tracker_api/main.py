from fastapi import FastAPI , HTTPException
from pydantic import BaseModel
from data import expenses

app = FastAPI()


class Expense(BaseModel):
    title: str
    amount: float
    category: str


@app.get("/")
def home():
    return {"message": "Expense Tracker API is running!"}


@app.get("/expenses")
def get_expenses():
    return expenses

@app.post("/expenses")
def create_expense(expense : Expense):
    
    new_expense = expense.model_dump()
    
    new_expense['id'] = len(expenses) + 1
    
    expenses.append(new_expense)
    
    return new_expense

@app.get("/expenses/{expense_id}")
def get_expense(expense_id: int):
    for expense in expenses:
        if expense["id"] == expense_id:
            return expense

    raise HTTPException(status_code=404, detail='Expense not found')
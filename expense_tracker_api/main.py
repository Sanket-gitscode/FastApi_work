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
    
    new_expense["id"] = max([expense["id"] for expense in expenses], default=0) + 1
    
    expenses.append(new_expense)
    
    return new_expense

@app.get("/expenses/{expense_id}")
def get_expense(expense_id: int):
    for expense in expenses:
        if expense["id"] == expense_id:
            return expense

    raise HTTPException(status_code=404, detail='Expense not found')

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    for expense in expenses:
        if expense["id"] == expense_id:
            expenses.remove(expense)
            return {"message": "Expense deleted successfully"}

    raise HTTPException(status_code=404, detail="Expense not found")

@app.put("/expenses/{expense_id}")
def update_expense(expense_id: int, updated_expense: Expense):
    for expense in expenses:
        if expense["id"] == expense_id:
            expense["title"] = updated_expense.title
            expense["amount"] = updated_expense.amount
            expense["category"] = updated_expense.category

            return expense

    raise HTTPException(status_code=404, detail="Expense not found")
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from database import Base, engine, SessionLocal
from models import Expense


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI()


# -------------------------
# Pydantic Models
# -------------------------

# Data sent by the client when creating/updating an expense
class ExpenseCreate(BaseModel):
    title: str = Field(min_length=3)
    amount: float = Field(gt=0)
    category: str = Field(min_length=3)


# Data returned by the API
class ExpenseResponse(BaseModel):
    id: int
    title: str
    amount: float
    category: str


# -------------------------
# Home
# -------------------------

@app.get("/")
def home():
    return {
        "message": "Expense Tracker API is running!"
    }


# -------------------------
# Get All Expenses
# -------------------------

@app.get("/expenses", response_model=list[ExpenseResponse])
def get_expenses(
    category: str | None = None,
    min_amount: float | None = None,
    max_amount: float | None = None
):

    db = SessionLocal()

    expenses = db.query(Expense).all()

    db.close()

    # Apply category filter
    if category is not None:
        expenses = [
            expense
            for expense in expenses
            if expense.category == category
        ]

    # Apply minimum amount filter
    if min_amount is not None:
        expenses = [
            expense
            for expense in expenses
            if expense.amount >= min_amount
        ]

    # Apply maximum amount filter
    if max_amount is not None:
        expenses = [
            expense
            for expense in expenses
            if expense.amount <= max_amount
        ]

    return expenses


# -------------------------
# Create Expense
# -------------------------

@app.post("/expenses", response_model=ExpenseResponse)
def create_expense(expense: ExpenseCreate):

    db = SessionLocal()

    new_expense = Expense(
        title=expense.title,
        amount=expense.amount,
        category=expense.category
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    db.close()

    return new_expense


# -------------------------
# Get Single Expense
# -------------------------

@app.get("/expenses/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: int):

    db = SessionLocal()

    expense = db.query(Expense).filter(
        Expense.id == expense_id
    ).first()

    db.close()

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return expense


# -------------------------
# Update Expense
# -------------------------

@app.put("/expenses/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    updated_expense: ExpenseCreate
):

    db = SessionLocal()

    expense = db.query(Expense).filter(
        Expense.id == expense_id
    ).first()

    if expense is None:
        db.close()

        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    expense.title = updated_expense.title
    expense.amount = updated_expense.amount
    expense.category = updated_expense.category

    db.commit()
    db.refresh(expense)

    db.close()

    return expense


# -------------------------
# Delete Expense
# -------------------------

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):

    db = SessionLocal()

    expense = db.query(Expense).filter(
        Expense.id == expense_id
    ).first()

    if expense is None:
        db.close()

        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    db.delete(expense)
    db.commit()

    db.close()

    return {
        "message": "Expense deleted successfully"
    }
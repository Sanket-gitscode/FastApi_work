from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello World"}

@app.get("/about")
def about():
    return {"message": "This is my FastAPI project"}

@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Hello {name}"}

class User(BaseModel):
    name : str
    age  : int
    

@app.post("/users")
def create_user(user : User):
    return {
        "message" :  "User created successfully",
        "user" : user
    }


@app.get("/search")
def search(name: str):
    return {"message": f"Searching for {name}"}

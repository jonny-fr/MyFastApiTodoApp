import bcrypt
from fastapi import FastAPI
from pydantic import BaseModel
import json
from typing import List
from bcrypt import hashpw, gensalt

app = FastAPI()

# Initialize todos list
try:
    with open("todos.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        todos: List[dict] = data if isinstance(data, list) else []
except FileNotFoundError:
    print("File 'todos.json' not found. Using an empty list.")
    todos = []
except json.JSONDecodeError as e:
    print(f"Error parsing JSON file: {e}")
    todos = []
except IOError as e:
    print(f"Error reading the file: {e}")
    todos = []

# Initialize user list
try:
    with open("users.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        users: List[dict] = data if isinstance(data, list) else []
except FileNotFoundError:
    print("File 'todos.json' not found. Using an empty list.")
    users = []
except json.JSONDecodeError as e:
    print(f"Error parsing JSON file: {e}")
    users = []
except IOError as e:
    print(f"Error reading the file: {e}")
    users = []



# Save todos to file
def save_user():
    try:
        with open("users.json", "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Error writing to the file: {e}")


# Save todos to file
def save_todos():
    try:
        with open("todos.json", "w", encoding="utf-8") as f:
            json.dump(todos, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Error writing to the file: {e}")

class TodoItem(BaseModel):
    todo: str

class User(BaseModel):
    username: str
    password: str

@app.post("/todos")
async def create_todo(todo_item: TodoItem):
    todos.append(todo_item.dict())
    save_todos()
    return {"message": "Todo created successfully", "todo": todo_item.todo}


@app.post("/register")
async def register_user(user: User):
    # Check if the user already exists
    for existing_user in users:
        if existing_user["username"] == user.username:
            return {"error": "User already exists"}, 400

    # Hash the password
    hashed_password = hashpw(user.password.encode('utf-8'), gensalt()).decode('utf-8')

    # Add the new user to the list with the hashed username
    users.append({"username": user.username, "password": hashed_password})
    save_user()
    return {"message": "User registered successfully", "user": user.username}

@app.post("/login")
async def login_user(user: User):
    # Check if the user exists
    for existing_user in users:
        if existing_user["username"] == user.username:
            # Verify the password
            if bcrypt.checkpw(user.password.encode('utf-8'), existing_user["password"].encode('utf-8')):
                return {"message": "Login successful", "user": user.username}
            else:
                return {"error": "Invalid password"}, 400

    return {"error": "User not found"}, 404



@app.get("/todos")
async def get_todos():
    return {"todos": todos}

@app.get("/todos/{todo_id}")
async def get_todo(todo_id: int):
    if 0 <= todo_id < len(todos):
        return {"todo": todos[todo_id]}
    else:
        return {"error": "Todo not found"}, 404

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

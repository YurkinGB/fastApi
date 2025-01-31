from typing import Annotated

from fastapi import FastAPI, HTTPException, Path

app = FastAPI()

# Инициализируем словарь users
users = {'1': 'Имя: Example, возраст: 18'}


# GET запрос для получения всех пользователей
@app.get('/users')
async def get_users():
    return users


# POST запрос для добавления нового пользователя
@app.post('/user/{username}/{age}')
async def add_user(username: Annotated[str, Path(min_length=2, max_length=15, example="name")],
                   age: Annotated[int, Path(ge=18, le=100, example=18)]):
    global users
    if not users:
        new_id = '1'
    else:
        new_id = str(max(map(int, users.keys())) + 1)
    users[new_id] = f'Имя: {username}, возраст: {age}'
    return f"User {new_id} is registered"


# PUT запрос для обновления существующего пользователя
@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: Annotated[int, Path(ge=1, description="User ID", example=1)],
                      username: Annotated[str, Path(min_length=2, max_length=15, description="Имя", example="user")],
                      age: Annotated[int, Path(ge=18, le=100, description="Возраст", example=18)]):
    if str(user_id) not in users:
        raise HTTPException(status_code=404, detail="User not found")
    users[user_id] = f'Имя: {username}, возраст: {age}'
    return f"The user {user_id} is updated"


# DELETE запрос для удаления пользователя
@app.delete('/user/{user_id}')
async def delete_user(user_id: Annotated[int, Path(ge=1, description="User ID", example=1)]):
    if str(user_id) not in users:
        raise HTTPException(status_code=404, detail="User not found")
    del users[str(user_id)]
    return f"The user {user_id} is deleted"

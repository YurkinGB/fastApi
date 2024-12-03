from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()


users = {'1': 'Имя: Example, возраст: 18'}


@app.get("/users")
async def get_users() -> dict:
    return users


@app.post("/user/{username}/{age}")
async def post_user(username: Annotated[str, Path(min_length=2, max_length=15, description="Имя", example="user")],
                    age: Annotated[int, Path(ge=18, le=100,description="Возраст", example=18)]) -> str:
    index = str(int(max(users, key=int)) + 1)
    users[index] = f'Имя: {username}, возраст: {age}'
    return f'User {index} is registered'


@app.put("/user/{user_id}/{username}/{age}")
async def put_user(user_id: Annotated[int, Path(ge=1, description="User ID", example=1)],
                   username: Annotated[str, Path(min_length=2, max_length=15, description="Имя", example="user")],
                   age: Annotated[int, Path(ge=18, le=100,description="Возраст", example=18)]) -> str:
    users[str(user_id)] = f'Имя: {username}, возраст: {age}'
    return f'The user {user_id} is updated'


@app.delete("/user/{user_id}")
async def delete_user(user_id: Annotated[int, Path(ge=1, description="User ID", example=1)]):
    users.pop(str(user_id))

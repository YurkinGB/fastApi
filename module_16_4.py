from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()


users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int = None


@app.get("/users")
async def get_users() -> List[User]:
    return users


@app.post("/user/{username}/{age}")
async def post_user(username: Annotated[str, Path(min_length=2, max_length=15, example="name")],
                    age: Annotated[int, Path(ge=18, le=100, example=18)]) -> User:
    if not users:
        new_user = User(id=1, username=username, age=age)
        users.append(new_user)
    else:
        user_id = users[-1].id + 1
        new_user = User(id=user_id, username=username, age=age)
        users.append(new_user)
    return new_user


@app.put("/user/{user_id}/{username}/{age}")
async def put_user(user_id: Annotated[int, Path(ge=1, description="User ID", example=1)],
                   username: Annotated[str, Path(min_length=2, max_length=15, description="Имя", example="user")],
                   age: Annotated[int, Path(ge=18, le=100, description="Возраст", example=18)]) -> User:
    for user in users:
        if user_id == user.id:
            user.username = username
            user.age = age
            return user
    else:
        raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}")
async def delete_user(user_id: Annotated[int, Path(ge=1, description="User ID", example=1)]) -> User:
    for i in range(len(users)):
        if users[i].id == user_id:
            return users.pop(i)
    else:
        raise HTTPException(status_code=404, detail="User was not found")

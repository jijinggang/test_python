import fastapi
from pydantic import BaseModel
app = fastapi.FastAPI()


class User(BaseModel):
    name: str
    sex: bool
    age: int


users = {}


@app.get('/')
def root():
    return {
        'users': users
    }


@app.get('/user/{id}')
def getuser(id: int):

    return {'id': id, 'user': users[id]}


@app.put('/user/{id}')
def putuser(id: int, user: User):
    users[id] = user
    return {'id': id, 'user': user}

# pip install uvicorn fastapi
# start
# uvicorn test_fastapi:app --reload

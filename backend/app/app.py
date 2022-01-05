from fastapi import FastAPI, HTTPException
from mongoengine.errors import NotUniqueError
from mongoengine.queryset.transform import update
from starlette.requests import Request
from mongoengine import connect
connect(db="project",host="localhost",port=27017)

from app.models import (UserIn,UserIn_PY,Item,Item_PY,Value,Value_PY,Image,Image_PY)
from app.crud_fun import add_item, remove_item, retrive_item,retrive_items, update_item
app = FastAPI()

origins=["http://localhost:3000"]

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)


@app.post("/user/", response_model=UserIn_PY)
async def create_user(user: UserIn_PY):
    users=UserIn(**user.dict())
    try:
        users.save()
    except NotUniqueError:
        raise HTTPException(status_code=404,detail="This user already registered")
    return user



@app.post("/items/",response_model=Item_PY)
def create_item(item: Item_PY,request:Request):
    if request:
        add_item(item)
        return item

@app.get('/get_items')
def get_items(request: Request):
    if request:
        item= retrive_items()
        context={"response":item}
        return context

@app.get('/get_item/{id}')
def get_item(id:str, request: Request):
    if request:
        return retrive_item(id)

@app.put('/update_item/{id}')
def put_item(id:str,item: Item_PY,request:Request):
    if request:
        return update_item(id,item)

@app.delete('/delete_item/{id}')
def delete_item(id:str,request:Request):
    if request:
        return remove_item(id)
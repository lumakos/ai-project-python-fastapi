from fastapi import FastAPI, Query, Path, Form
from enum import Enum
from pydantic import BaseModel, Field
from typing import Annotated

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None

class User(BaseModel):
    username: str
    full_name: str | None = None

class FormData(BaseModel):
    username: str
    password: str


@app.post("/login/")
async def login(data: Annotated[FormData, Form()]):
    return data

@app.get("/")
def root():
    return {"msg": "FastAPI with Python 3.13 and fastapi dev 🚀"}

@app.get("/users/me", status_code = 200)
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Annotated[str | None, Query(min_length=3, max_length=50)] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

@app.post("/items/", status_code = 201)
async def create_item(item: Item) -> Item:
    item_dict = item.dict()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

@app.get("/cats/")
async def read_cats(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results
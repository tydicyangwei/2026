from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": None},
}

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    item = items[item_id]
    json_compatible_item_data = jsonable_encoder(item)
    return json_compatible_item_data

@app.put("/items/{item_id}")
async def update_item(item_id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
 #   json_compatible_item_data = item.model_dump()
    items[item_id] = json_compatible_item_data
    return items[item_id]

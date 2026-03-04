from fastapi import FastAPI
from pydantic import BaseModel,HttpUrl
app = FastAPI()
class Image(BaseModel):
    url: HttpUrl
    name: str
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tag: list[str] = []
    image: Image | None = None
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results

@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    return weights

@app.post("/images/multiple/")
async def create_multiple_images(images: list[str]):
    return images

"""
/items/{item_id}请求体示例：
{
    "name": "yangwei",
    "description": "666",
    "price": "100.1",
    "tax": "2",
    "tag": ["one","two"],
    "image": {
        "url": "https://www.baidu.com",
        "name": "baidu"
    }
}

/index-weights/请求体示例：
{
    "1": 0.1,
    "2": 0.2,
    "3": 0.3
}
/images/multiple/请求体示例：
[
    "test1",
    "test2"
]

"""
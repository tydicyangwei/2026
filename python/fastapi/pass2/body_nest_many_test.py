from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    images: list[Image] | None = None


class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]


@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer

"""
请求体示例：
{
    "name": "yangwei",
    "description": "666",
    "price": "100.1",
    "items": [
        {
            "name": "yangwei",
            "description": "666",
            "price": "100.1",
            "tax": "2",
            "tags": ["one", "two"],
            "images": [
                {
                    "url": "https://www.baidu.com",
                    "name": "baidu"
                }
            ]
        }
    ]
}
"""

from typing import Annotated
from fastapi import FastAPI, Body, Path
from pydantic import BaseModel, Field
app = FastAPI()
class Item(BaseModel):
    name: str = Field(title="The name of the item", max_length=300)
    description: str | None = Field(
        None, title="A description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = Field(
        None, gt=0, description="The tax must be greater than zero"
    )
@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str | None = None,
    item: Item | None = Body(
        Embed=True,
        title="The item to update",
        description="The item to update with all its information",
    ),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results

from typing import Annotated
from fastapi import FastAPI,Path,Query
app = FastAPI()
@app.get("/items/{item_id}")
async def read_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=1)],
    q: Annotated[str | None, Query(title="Query string for the items to search in the database that have a good match")]=None,
):
    result = {"item_id": item_id}
    if q:
        result.update({"q": q})
    return result

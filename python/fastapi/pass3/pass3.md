## 第三课

### 处理错误

* error_test.py
fastapi默认异常类：HTTPException
自定义响应header头

自定义异常处理器
* def_exception_test.py

* 使用自定义类或第三方类覆盖fastapi默认的异常类
```javascript
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

#覆盖默认的HTTPException
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

#覆盖默认的RequestValidationError类
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    message = "Validation errors:"
    for error in exc.errors():
        message += f"\nField: {error['loc']}, Error: {error['msg']}"
    return PlainTextResponse(message, status_code=400)


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}
```

### 路径操作配置
路径参数
#### 小结
* 通过传递参数给路径操作装饰器，即可轻松地配置路径操作、添加元数据。

### json兼容编码器
jsonable_encoder
* jsonable_encoder_test.py

#### 注意
* jsonable_encoder实际上是FastAPI内部用来转换数据的。但是它在许多其他场景中也很有用。


### 请求体更新数据
* request_update_test.py
使用put替换更新
```javascript
@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded
```
使用patch部分更新
```javascript
@app.patch("/items/{item_id}")
async def update_item(item_id: str, item: Item) -> Item:
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)  ##将原始数据转成pydantic模型
    update_data = item.model_dump(exclude_unset=True)  ##dump用户数据成python类型
    updated_item = stored_item_model.model_copy(update=update_data)  ##复制原始数据并用用户数据去更新
    items[item_id] = jsonable_encoder(updated_item)   ##转成python格式更新原始字典数据
    return updated_item
```





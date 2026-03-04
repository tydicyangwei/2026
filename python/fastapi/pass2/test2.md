## 第二课
尽量使用typing的Annotated申明参数的相关属性。

### 请求体
* Pydantic
```javascript
from pydantic import BaseModel, Field, ValidationError

class User(BaseModel):
    id: int
    name: str = Field(..., min_length=1)
    age: int = Field(ge=0, le=150)

try:
    user = User(id="123", name="Alice", age=30)  # id 自动转为 int
    print(user.model_dump_json())  # {"id":123,"name":"Alice","age":30}
except ValidationError as e:
    print(e)
```
* body_test.py

### 查询参数及校验
* find_check_test.py

### 路径参数及校验
* path_check_test.py

### 查询参数及模型
* find_model_test.py

### 请求体及多个参数混合
* body_many_test.py

### 请求体及字段
* body_field_test.py

### 请求体及嵌套
* body_nest_test.py
* 多层嵌套 body_nest_many_test.py

### 额外参数类型
* extra_test.py
* uuid.UUID
* datetime.datetime datetime.time datatime.timedelta

### cookie
* cookie_test.py

### header
* header_test.py
默认会把header类型参数的"_"转为"-"
可以通过list[str]定义多个请求头

### cookie参数模型
* cookie_model_test.py

### header参数模型
基本原理同上面"cookie参数模型"

### 响应模型
* response_model_test.py
通过response_model参数使函数返回的参数跟函数注释的返回类型不一致（以response_model参数为准）。
* 通过继承的方式实现如下
```javascript
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()

class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(BaseUser):
    password: str

@app.post("/user/")
async def create_user(user: UserIn) -> BaseUser:
    return user
```

* response_test.py
如下代码中，装饰器函数的response_model_exclude_unset可以使返回的对象中，排查未设置的对象，还有类似的参数如：response_model_exclude_defaults、response_model_exclude_none、response_model_include
```javascript
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}

@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]
```

#### 总结
* 使用路径操作装饰器的 response_model 参数来定义响应模型，尤其是确保私有数据被过滤掉。
* 使用 response_model_exclude_unset 来仅返回显式设置的值。

### 更多模型
* many_model_test.py
* many_model_union_test.py

```javascript
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str


items = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "There goes my enemy"},
]


@app.get("/items/", response_model=list[Item])
async def read_items():
    return items
```
#### 总结
* 针对不同场景，可以随意使用不同的 Pydantic 模型并通过继承复用,当一个实体需要具备不同的状态时，无需只为该实体定义一个数据模型。例如，用户实体就可能有包含 password、包含 password_hash 以及不含密码等多种状态。


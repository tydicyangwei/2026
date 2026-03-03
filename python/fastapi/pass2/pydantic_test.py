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
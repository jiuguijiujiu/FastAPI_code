from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

# 需求：注册：用户名和密码 → str
# 创建 请求体参数 类
class User(BaseModel):
    name: str = Field(default='小米', min_length=2, max_length=10, description='用户名，长度范围：2-10')
    password: str = Field(min_length=3, max_length=20)

@app.post('/register')
async def register(user: User):     # 类型注解，使用请求体参数
    return user
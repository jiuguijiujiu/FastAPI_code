# 导包
from fastapi import FastAPI

# 1. 创建 FastAPI 实例
app = FastAPI()

# 2. API接口1
@app.get("/")                            # 目录位置
async def root():                        # async：异步
    return {"message": "Hello World"}    # 返回值

# 2. API接口2
@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
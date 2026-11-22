from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

# 接口： 返回一张图片内容
@app.get('/file')
async def get_file():
    return FileResponse('./data/1.jpeg')
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# 接口 → 响应 HTML 代码
@app.get(path="/html", response_class=HTMLResponse)
async def get_html():
    return "<h1>这是一级标题</h1>"
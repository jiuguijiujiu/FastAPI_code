from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


# 自定义格式 类
# 需求：新闻接口 → 响应数据格式 id、title、content
class News(BaseModel):
    id: int
    title: str
    content: str


@app.get(path='/news/{book_id}', response_model=News)        # 设置输出为自定义格式
async def get_news(book_id: int):
    return {
        'id': book_id,
        'title': f'这本书id为{book_id}',
        'content': '这是一本好书'
    }

from fastapi import FastAPI, Path

app = FastAPI()

@app.get('/book/{book_id}')
async def get_book_id(book_id: int = Path(..., gt=0, lt=101, description='书籍id取值范围：1-100')):
    return {'id': book_id, 'title': f"这本书id为{book_id}"}

# 需求：查找书籍的作者，路径参数 name，长度范围 2-10
@app.get('/author/{name}')
async def get_name(name: str = Path(..., min_length=2, max_length=10, description='作者名长度范围：2-10')):
    return {'msg': f'这是{name}的信息'}
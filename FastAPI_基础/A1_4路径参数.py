from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'Hello World'}

@app.get('/book/{book_id}')
async def get_book(book_id: int):
    return {"id": book_id, "title": f"这本书的id为{book_id}"}
from fastapi import FastAPI, HTTPException

app = FastAPI()

# 需求：按 id 查询新闻 -> 1 - 6
@app.get('/news/{new_id}')
async def get_new(new_id: int):
    id_list = [1, 2, 3, 4, 5, 6]
    if new_id not in id_list:
        raise HTTPException(status_code=404, detail="您查找的新闻不存在")
    return {'id': new_id}
from fastapi import FastAPI

app = FastAPI()

@app.middleware('http')
async def middleware2(request, call_next):
    print('中间件2开始工作-start')
    response = await call_next(request)
    print('中间件2结束工作-end')
    return response

@app.middleware('http')
async def middleware1(request, call_next):
    print('中间件1开始工作-start')
    response = await call_next(request)
    print('中间件1结束工作-end')
    return response

@app.get("/")
async def root():
    return {"message": "Hello World"}
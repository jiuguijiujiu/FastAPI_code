from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from sqlalchemy import DateTime, func, Float, String, Integer, select

app = FastAPI()

# 1. 准备异步数据库URL
ASYNC_DATABASE_URL = 'mysql+aiomysql://root:123456@localhost:3306/fast_api?charset=utf8'
# 2. 创建异步引擎(相当于创建数据库对象)
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo = True,              # 可选，输出 SQL 日志
    pool_size = 10,           # 设置连接池活跃的连接数
    max_overflow = 20         # 允许额外的连接数
)

# 3. 定义类： 表的基类 + 表的具体类（相当于设置表的格式）
# 基类：创建时间、更新时间
class Base(DeclarativeBase):
    # 设置基础字段
    # Mapped[datetime]：告诉 Python 和 IDE，这个由mapped创建的字段 是标准的时间对象（datetime），且必填
    # DateTime：告诉数据库，底层建表时，该字段用DateTime类型
    # insert_default=func.now(),：告诉数据库，底层插入数据时，这字段如果内没有赋值，默认插入时间，用数据库的func工具查询时间
    # default=func.now：告诉 SQLAlchemy 框架，“在 Python 端生成 SQL 之前，如果没赋值，就调用 func.now 函数生成一个时间”（注意：这里没加括号，传的是函数对象，SQLAlchemy 会在需要时自己调）
    create_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), default=func.now, comment='创建时间')
    # onupdate=func.now()：只要这条数据被修改（执行了 UPDATE 操作），数据库都会自动把这个字段的值更新为当前时间
    update_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), default=func.now, onupdate=func.now(), comment='更新时间')

# 书籍类：id、书名、作者、价格、出版社
class Book(Base):
    # 设置表名
    __tablename__ = 'book'
    # 设置字段
    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment='书籍id')
    book_name: Mapped[str] = mapped_column(String(255), comment='书名')
    author: Mapped[str] = mapped_column(String(255), comment='作者')
    price: Mapped[float] = mapped_column(Float, comment='价格')
    publisher: Mapped[str] = mapped_column(String(255), comment='出版社')

# 4. 建表：定义建表函数 → FastAPI 启动的时候调用建表的函数
async def create_table():
    # 开启异步引擎
    async with async_engine.begin() as conn:
        # 建表
        await conn.run_sync(Base.metadata.create_all)   # 创建 Base类的元数据

@app.on_event('startup')
async def startup_event():
    await create_table()

@app.get('/')
async def root():
    return {'message': '服务已启动'}


# 需求：创建查询功能的接口，查询图书 → 依赖注入：创建依赖项获取数据库会话 + Depends 注入路由处理函数
# 创建数据库会话对象(相当于获取数据库中表的所有数据)
AsyncSessionLocal = async_sessionmaker(
    bind = async_engine,                        # 绑定数据库引擎
    class_ = AsyncSession,                      # 指定会话类
    expire_on_commit = False                    # 提交后会话不过期，不会重新查询数据库
)

# 创建依赖项
async def get_database():
    # 开启数据库会话
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()      # 提交：保存表的修改
        except Exception:
            await session.rollback()    # 有异常，回滚：撤销表的修改
            raise
        finally:
            await session.close()       # 关闭会话

@app.get('/book/count')
async def get_count(db: AsyncSession = Depends(get_database)):
    # 聚合查询 select( func.方法名(模型类.属性) )
    # result = await db.execute(select(func.count(Book.id)))
    # result = await db.execute(select(func.max(Book.price)))
    # result = await db.execute(select(func.sum(Book.price)))
    result = await db.execute(select(func.avg(Book.price)))
    num = result.scalar()                                       # 用来提取一个数值 → 标量值
    return num
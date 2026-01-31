
from fastapi import FastAPI, WebSocket

from longtask_router import longtask_router


app = FastAPI()

app.include_router(longtask_router)


if __name__ == "__main__":
    import uvicorn
    # "path" 是模块所在的目录或包。
    # "main" 是模块的名字（文件名）。
    # "app" 是 FastAPI 实例的名称（你在代码中定义的 FastAPI() 实例）。
    # uvicorn.run("path/main:app", host="0.0.0.0", port=8000)
    uvicorn.run(app, host="0.0.0.0", port=8000)
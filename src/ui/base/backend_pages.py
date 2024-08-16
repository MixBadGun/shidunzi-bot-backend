"""
后端将数据暴露给前端的接口定义，以及将模板显示出来的定义
"""

import uuid
from pathlib import Path

import nonebot
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from nonebot.drivers.fastapi import Driver as FastAPIDriver
from pydantic import BaseModel


class BackendDataManager:
    data: dict[str, BaseModel]

    def __init__(self) -> None:
        self.data = {}

    def register(self, data: BaseModel) -> str:
        """
        往数据管理器中注册一些数据，返回这个数据的识别 ID
        """
        _id = uuid.uuid4().hex
        self.data[_id] = data
        return _id

    def get(self, data_id: str) -> BaseModel | None:
        """
        获得数据
        """
        return self.data.get(data_id, None)


_nb_driver = nonebot.get_driver()

assert isinstance(_nb_driver, FastAPIDriver)


app = _nb_driver.server_app
manager = BackendDataManager()
router = APIRouter()


def backend_register_data(data: BaseModel) -> str:
    return manager.register(data)


@router.get("/data/{data_id}/")
async def request_data(data_id: str):
    data = manager.get(data_id)
    if data is None:
        return {"status": "failed", "detail": "所请求的 data_id 不存在"}
    return {"status": "success", "detail": "", "data": data}


@router.get("/html/{file_name}/")
async def request_html(file_name: str):
    fp = Path("./res/html/") / (file_name + ".html")
    code = 200
    if not fp.exists():
        fp = Path("./res/html/") / "404.html"
        code = 404
    return HTMLResponse(fp.read_text(encoding="utf-8"), code)


app.include_router(router, prefix="/kagami")

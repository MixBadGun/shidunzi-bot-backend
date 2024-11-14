from pydantic import BaseModel

from src.ui.types.common import GetAward, UserData


class ZhuaMeta(BaseModel):
    field_from: int
    get_chip: str
    own_chip: str
    remain_time: str
    max_time: str
    need_time: str


class ZhuaData(BaseModel):
    user: UserData
    meta: ZhuaMeta
    catchs: list[GetAward]

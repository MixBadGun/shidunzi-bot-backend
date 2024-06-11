from pydantic import BaseModel
from nonebot import get_plugin_config


class Config(BaseModel):
    """Plugin Config Here"""

    # 对 Bot 拥有绝对管理权的管理员（一员）
    admin_id: int = -1

    # 允许管理 Bot 的小哥库等的各种事项的群
    admin_groups: list[int] = []

    # 在发送「小镜！！！」的时候，遇到特殊的 QQ 号，回复特殊的内容
    custom_replies: dict[str, str] = {}

    # 对于「小镜！！！」后面的正则表达式匹配规则，这里不应该设置太宽泛，以免出现意料之外的消息
    re_match_rule: str = "^[!！?？。.,， 1;；：:'‘’\"“”]+$"

    # 是否预先画好小哥的图片
    predraw_images: bool = False


config = get_plugin_config(Config)

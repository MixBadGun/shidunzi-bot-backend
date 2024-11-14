from typing import Any

from arclet.alconna import Alconna, Arg, ArgFlag, Arparma, Option

from src.base.command_events import MessageContext
from src.common.command_deco import (
    listen_message,
    match_alconna,
    require_admin,
)
from src.core.unit_of_work import get_unit_of_work

@listen_message()
@require_admin()
@match_alconna(
    Alconna(
        ["::"],
        "炸毁全服"
    )
)
async def _(ctx: MessageContext, res: Arparma[Any]):
    async with get_unit_of_work() as uow:
        for uid in await uow.users.all_users():
            await uow.inventories.clear_inventory(uid)

    await ctx.reply("炸了。")

from typing import Any

from arclet.alconna import Alconna, Arg, ArgFlag, Arparma, MultiVar, Option
from nonebot_plugin_alconna import At, Image

from src.base.command_events import GroupContext, OnebotContext
from src.base.exceptions import ObjectAlreadyExistsException, ObjectNotFoundException
from src.common.data.awards import download_award_image, get_a_list_of_award_storage
from src.common.decorators.command_decorators import (
    listenGroup,
    listenOnebot,
    matchAlconna,
    requireAdmin,
    withLoading,
)
from src.common.lang.zh import la
from src.core.unit_of_work import UnitOfWork, get_unit_of_work
from src.models.level import level_repo
from src.ui.pages.storage import render_progress_message, render_storage_message
from src.ui.views.list_view import UserStorageView
from src.ui.views.user import UserData


@listenOnebot()
@requireAdmin()
@matchAlconna(
    Alconna(
        "小哥",
        ["::添加", "::创建"],
        Arg("name", str),
        Arg("level", str),
    )
)
async def _(ctx: OnebotContext, res: Arparma):
    aname = res.query[str]("name")
    lname = res.query[str]("level")
    assert aname is not None
    assert lname is not None

    async with get_unit_of_work() as uow:
        aid = await uow.awards.get_aid(aname)
        if aid is not None:
            raise ObjectAlreadyExistsException(aname)
        level_obj = level_repo.get_by_name(lname)
        if level_obj is None:
            raise ObjectNotFoundException("等级", lname)
        await uow.awards.add_award(aname, level_obj.lid)
    await ctx.reply("ok.")


@listenOnebot()
@requireAdmin()
@matchAlconna(
    Alconna(
        "小哥",
        ["::删除", "::移除"],
        Arg("name", str),
    )
)
async def _(ctx: OnebotContext, res: Arparma):
    name = res.query[str]("name")
    assert name is not None

    async with get_unit_of_work() as uow:
        aid = await uow.awards.get_aid_strong(name)
        await uow.awards.delete_award(aid)
    await ctx.reply("ok.")


@listenOnebot()
@requireAdmin()
@matchAlconna(
    Alconna(
        "re:(修改|更改|调整|改变|设置|设定)小哥",
        ["::"],
        Arg("小哥原名", str),
        Option(
            "名字",
            Arg("小哥新名字", str),
            alias=["--name", "名称", "-n", "-N"],
            compact=True,
        ),
        Option(
            "等级",
            Arg("等级名字", str),
            alias=["--level", "级别", "-l", "-L"],
            compact=True,
        ),
        Option(
            "描述",
            Arg("描述", MultiVar(str, flag="+"), seps="\n"),
            alias=["--description", "-d", "-D"],
            compact=True,
        ),
        Option("图片", Arg("图片", Image), alias=["--image", "照片", "-i", "-I"]),
        Option(
            "特殊性",
            Arg("特殊性", str),
            alias=["--special", "特殊", "-s", "-S", "是否特殊"],
        ),
        Option(
            "排序优先度",
            Arg("排序优先度", int),
            alias=["--priority", "优先度", "-p", "-P"],
        ),
    )
)
async def _(ctx: OnebotContext, res: Arparma):
    name = res.query[str]("小哥原名")
    newName = res.query[str]("小哥新名字")
    levelName = res.query[str]("等级名字")
    _description = res.query[tuple[str]]("描述") or ()
    image = res.query[Image]("图片")
    special = res.query[str]("特殊性")
    sorting = res.query[int]("排序优先度")
    if name is None:
        return

    async with get_unit_of_work() as uow:
        aid = await uow.awards.get_aid_strong(name)
        lid = (
            uow.levels.get_by_name_strong(levelName).lid
            if levelName is not None
            else None
        )
        special = special in ("是", "1", "true", "t", "y", "yes")
        image = image.url if image is not None else None
        image = await download_award_image(aid, image) if image is not None else None
        await uow.awards.modify(
            aid=aid,
            name=newName,
            description="".join(_description),
            lid=lid,
            image=image,
            special=special,
            sorting=sorting,
        )

    await ctx.reply("ok.")


@listenGroup()
@requireAdmin()
@matchAlconna(Alconna(["::"], "给薯片", Arg("对方", int), Arg("数量", int)))
async def _(ctx: GroupContext, res: Arparma[Any]):
    target = res.query("对方")
    number = res.query[int]("数量")
    if target is None or number is None:
        return
    assert isinstance(target, int)

    async with get_unit_of_work() as uow:
        uid = await uow.users.get_uid(target)
        await uow.users.add_money(uid, number)

    await ctx.reply("给了。", at=False, ref=True)


@listenOnebot()
@requireAdmin()
@matchAlconna(Alconna(["::"], "全部给薯片", Arg("数量", int)))
async def _(ctx: OnebotContext, res: Arparma[Any]):
    number = res.query[int]("数量")
    if number is None:
        return

    async with get_unit_of_work() as uow:
        for uid in await uow.users.all_users():
            await uow.users.add_money(uid, number)

    await ctx.reply("给了。", at=False, ref=True)


@listenGroup()
@requireAdmin()
@matchAlconna(
    Alconna(
        ["::"],
        "给小哥",
        Arg("对方", int),
        Arg("名称", str),
        Arg("数量", int, flags=[ArgFlag.OPTIONAL]),
    )
)
async def _(ctx: GroupContext, res: Arparma[Any]):
    target = res.query("对方")
    name = res.query[str]("名称")
    number = res.query[int]("数量")
    if target is None or name is None:
        return
    assert isinstance(target, int)

    if number is None:
        number = 1

    async with get_unit_of_work() as uow:
        uid = await uow.users.get_uid(target)
        aid = await uow.awards.get_aid_strong(name)
        await uow.inventories.give(uid, aid, number, False)

    await ctx.reply("给了。", at=False, ref=True)


async def get_storage_view(
    uow: UnitOfWork,
    userdata: UserData | None,
    level_name: str | None,
    show_notation1: bool = True,
    show_notation2: bool = True,
) -> UserStorageView:
    uid = None if userdata is None else userdata.uid
    view = UserStorageView(user=userdata)
    if level_name is not None:
        view.limited_level = uow.levels.get_by_name_strong(level_name)

    for level in uow.levels.sorted:
        if level_name is not None and level != view.limited_level:
            continue
        aids = await uow.awards.get_aids(level.lid)
        infos = await get_a_list_of_award_storage(
            uow,
            uid,
            aids,
            show_notation2=show_notation2,
            show_notation1=show_notation1,
        )
        view.awards.append((level, infos))
    return view


@listenOnebot()
@matchAlconna(
    Alconna(
        "re:(zhuajd|抓进度|抓小哥进度)",
        Option(
            "等级",
            Arg("等级名字", str),
            alias=["--level", "级别", "-l", "-L"],
            compact=True,
        ),
    )
)
@withLoading(la.loading.zhuajd)
async def _(ctx: OnebotContext, res: Arparma):
    levelName = res.query[str]("等级名字")
    async with get_unit_of_work(ctx.sender_id) as uow:
        view = await get_storage_view(
            uow,
            UserData(
                uid=await uow.users.get_uid(ctx.sender_id),
                name=await ctx.sender_name,
                qqid=str(ctx.sender_id),
            ),
            levelName,
        )

    await ctx.send(await render_progress_message(view))


@listenOnebot()
@matchAlconna(Alconna("re:(kc|抓库存|抓小哥库存)"))
@withLoading(la.loading.kc)
async def _(ctx: OnebotContext, _: Arparma):
    async with get_unit_of_work(ctx.sender_id) as uow:
        view = await get_storage_view(
            uow,
            UserData(
                uid=await uow.users.get_uid(ctx.sender_id),
                name=await ctx.sender_name,
                qqid=str(ctx.sender_id),
            ),
            None,
            show_notation2=False,
        )

    await ctx.send(await render_storage_message(view))


@listenOnebot()
@requireAdmin()
@matchAlconna(
    Alconna(
        "re:(所有|全部)小哥",
        ["::"],
        Option(
            "等级",
            Arg("等级名字", str),
            alias=["--level", "级别", "-l", "-L"],
            compact=True,
        ),
    )
)
@withLoading(la.loading.all_xg)
async def _(ctx: OnebotContext, res: Arparma):
    levelName = res.query[str]("等级名字")
    async with get_unit_of_work(ctx.sender_id) as uow:
        view = await get_storage_view(
            uow,
            None,
            levelName,
            show_notation1=False,
            show_notation2=False,
        )
    await ctx.send(await render_progress_message(view))

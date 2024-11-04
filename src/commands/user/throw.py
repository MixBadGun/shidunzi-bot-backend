import time

from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot_plugin_alconna import At, Emoji, Reply, Text, UniMessage

from src.base.command_events import OnebotContext
from src.common.command_deco import listen_message, require_awake
from src.common.data.awards import use_award
from src.common.rd import get_random
from src.core.unit_of_work import get_unit_of_work
from src.services.stats import StatService

FREQUENCY_LIMIT: dict[int, float] = {}


def generate_throw_message(sender_id: int, target: int, success: bool, count: int):
    msg = (
        UniMessage
        .at(user_id=str(sender_id))
        .text(" 向 ")
        .at(user_id=str(target))
        .text(" 丢出去了一个石墩子！")
    )
    if success:
        msg.text("\n丢中了！炸得 ").at(target).text(" 的库存是灰飞烟灭，寸草不生，万万石墩尽成灰！").image(path="./res/boom.png")
    else:
        msg.text(
            "可惜没扔中。"
        )
    # msg.text(f"（库存还有 {count} 个粑粑小哥）")
    return msg


async def analyze_throw_message(ctx: OnebotContext):
    is_throw = False
    is_poop = False
    target: set[int] = set()

    for segment in ctx.message:
        if isinstance(segment, Text):
            text = segment.text
            for i in (
                "石墩子"
            ):
                if i in text:
                    is_poop = True
            for i in ("丢", "扔", "抛", "吃", "赤", "吔", "叱", "持"):
                if i in text:
                    is_throw = True
            # 根据否定词的个数来判断是否表确定意义。
            nope_count = 0
            for i in ("不", "别", "莫", "讨厌", "勿"):
                nope_count += text.count(i)
            if nope_count % 2 == 1:
                return
        elif isinstance(segment, At):
            target.add(int(segment.target))
        elif isinstance(segment, Reply):
            if segment.origin is not None and isinstance(
                (msg := segment.origin), MessageSegment
            ):
                msgid: str | None = msg.data.get("id", None)
                if msgid is None:
                    continue
                res = await ctx.bot.call_api("get_msg", message_id=msgid)
                sender_obj = res.get("sender", None)
                if sender_obj is None:
                    return
                uid = sender_obj.get("user_id", None)
                if uid is None:
                    return
                target.add(int(uid))
        elif isinstance(segment, Emoji):
            if segment.id == "59":
                is_poop = True
        else:
            return

    if not is_throw or not is_poop or len(target) != 1:
        return

    return target.pop()


@listen_message()
@require_awake
async def _(ctx: OnebotContext):
    FREQUENCY_LIMIT.setdefault(ctx.sender_id, 0)
    if time.time() - FREQUENCY_LIMIT[ctx.sender_id] < 10:
        return
    FREQUENCY_LIMIT[ctx.sender_id] = time.time()

    target_qqid = await analyze_throw_message(ctx)

    if target_qqid is None:
        return
    if str(target_qqid) == ctx.bot.self_id:
        return
    if target_qqid == ctx.sender_id:
        # 如果是自己，就提示不能自丢。
        await ctx.reply(UniMessage.text("呀，你不能丢自己啊！"))
        return

    # 扔粑粑
    success = get_random().random() < 0.05

    async with get_unit_of_work(ctx.sender_id) as uow:
        fuid = await uow.users.get_uid(ctx.sender_id)
        tuid = await uow.users.get_uid(target_qqid)

        poop = await uow.awards.get_aid("石墩子")
        if poop is None:
            return
        await use_award(uow, fuid, poop, 1)
        if success:
            await uow.inventories.clear_inventory(tuid)

        count = await uow.inventories.get_storage(fuid, poop)
        stats = StatService(uow)
        await stats.throw_baba(fuid, tuid, success)

    await ctx.send(generate_throw_message(ctx.sender_id, target_qqid, success, count))

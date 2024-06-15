import time
from models import *
from src.db.crud import *
from src.common.db import AsyncSession


async def calculateTime(session: AsyncSession, user: User):
    """
    根据当前时间，重新计算玩家抓小哥的时间
    """

    globalConfig = await getGlobal(session)
    
    maxPickCount = user.pick_max_cache
    pickInterval = globalConfig.catch_interval
    now = time.time()

    if pickInterval == 0:
        user.pick_count_remain = maxPickCount
        user.pick_count_last_calculated = now
        return
    
    if user.pick_count_remain >= maxPickCount:
        user.pick_count_last_calculated = now
        return
    
    cycles = int((now - user.pick_count_last_calculated) / pickInterval)
    user.pick_count_last_calculated += cycles * pickInterval
    user.pick_count_remain += cycles

    if user.pick_count_remain > maxPickCount:
        user.pick_count_remain = maxPickCount
        user.pick_count_last_calculated = now


async def timeToNextCatch(session: AsyncSession, user: User):
    """
    计算玩家下一次抓小哥的时间，在调用这个方法前，请先调用 `calculateTime`。
    """

    globalConfig = await getGlobal(session)
    
    maxPickCount = user.pick_max_cache
    pickInterval = globalConfig.catch_interval

    now = time.time()

    if pickInterval == 0:
        return now
    
    if user.pick_count_remain >= maxPickCount:
        return now
    
    return user.pick_count_last_calculated + pickInterval

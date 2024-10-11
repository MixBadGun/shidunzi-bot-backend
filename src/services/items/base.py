from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from pydantic import BaseModel

from src.base.command_events import MessageContext
from src.base.exceptions import KagamiArgumentException, KagamiRangeError
from src.base.resources import Resource, static_res
from src.core.unit_of_work import UnitOfWork

T = TypeVar("T")


class UseItemArgs(BaseModel):
    count: int = 1
    target_uid: int | None = None

    def require_count_range(self, n_min: int | None = None, n_max: int | None = None):
        if n_min is not None and self.count < n_min:
            raise KagamiRangeError("物品数量", f"至少为 {n_min}", self.count)
        if n_max is not None and self.count > n_max:
            raise KagamiRangeError("物品数量", f"不超过 {n_max}", self.count)
        
    def require_target(self, required: bool = True):
        if required and self.target_uid is None:
            raise KagamiArgumentException("要制定一个人哦")
        elif not required and self.target_uid is not None:
            raise KagamiArgumentException("不用制定目标哦")


class BaseItem(BaseModel, Generic[T], ABC):
    """
    物品的基类。其中的泛型 T 是在函数间进行信息传输的量。
    在继承的时候，请使用泛型类的方式声明这个类型
    """

    name: str
    "物品的名字，同时会传入数据库作为物品的 ID"

    description: str
    "物品的描述"

    image: Resource = static_res("blank_placeholder.png")
    "物品的图片"

    item_sorting: float = 0.0
    """
    物品的排序顺序，会从小到大排序，小的在前，大的在后。
    如果你需要调整物品的排序，你可以更改这个字段，成随意的你认为的浮点值。
    """

    group: str
    """
    物品的物品组
    """

    @abstractmethod
    async def can_be_used(self, uow: UnitOfWork, uid: int, args: UseItemArgs) -> bool:
        """
        能否使用这个物品，如果需要更改逻辑，请重载这个函数
        """

    async def use_item_in_db(self, uow: UnitOfWork, uid: int, count: int):
        """
        在数据库中使用对应数量的当前物品
        """
        return await uow.items.use(uid, self.name, count)

    @abstractmethod
    async def use(self, uow: UnitOfWork, uid: int, args: UseItemArgs) -> T:
        """
        使用这个物品触发的逻辑，如果需要更改逻辑，请重载这个函数。
        在这里，你需要实现物品减少的逻辑，并告知用于你使用了这个物品的相关消息。
        """

    @abstractmethod
    async def send_use_message(self, ctx: MessageContext, data: T):
        """
        在这里，实现告知玩家物品使用结果的逻辑。
        """


class UnuseableItem(BaseItem[None]):
    async def can_be_used(self, uow: UnitOfWork, uid: int, args: UseItemArgs) -> bool:
        return False

    async def use(self, uow: UnitOfWork, uid: int, args: UseItemArgs) -> None:
        return None

    async def send_use_message(self, ctx: MessageContext, data: None):
        return None


class ItemInventoryDisplay(BaseModel):
    meta: BaseItem
    count: int = -1
    stats: int = -1


class ItemService:
    """
    物品服务
    """

    items: dict[str, BaseItem[Any]]

    def __init__(self) -> None:
        self.items = {}

    def register(self, item: BaseItem[Any]) -> None:
        assert (
            item.name not in self.items
        ), f"物品名 {item.name} 发生冲突了，请检查是否有重复注册"
        self.items[item.name] = item

    async def get_inventory_displays(
        self, uow: UnitOfWork, uid: int | None
    ) -> list[tuple[str, list[ItemInventoryDisplay]]]:
        """
        获得物品栏的展示清单，如果未提供 uid，则返回所有已经注册的物品。
        """

        _results: dict[str, list[ItemInventoryDisplay]] = {}

        if uid is not None:
            inventory = await uow.items.get_dict(uid)
            for key, (count, stats) in inventory.items():
                if key not in self.items:
                    continue
                item = self.items[key]
                _results.setdefault(item.group, [])
                _results[item.group].append(
                    ItemInventoryDisplay(
                        meta=item,
                        count=count,
                        stats=stats,
                    )
                )
        else:
            for item in self.items.values():
                _results.setdefault(item.group, [])
                _results[item.group].append(
                    ItemInventoryDisplay(
                        meta=item,
                    )
                )

        results = [(group, ls) for group, ls in _results.items()]
        results.sort(key=lambda result: result[0])
        return results


_global_service = ItemService()


def get_item_service() -> ItemService:
    """
    获得全局的物品管理服务
    """
    return _global_service


def register_item(item: BaseItem[Any]):
    """
    注册物品
    """
    get_item_service().register(item)

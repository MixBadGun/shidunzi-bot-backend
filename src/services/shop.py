from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.base.exceptions import ObjectNotFoundException
from src.base.res import KagamiResourceManagers
from src.base.res.resource import IResource
from src.core.unit_of_work import UnitOfWork


@dataclass
class ShopProductFreezed:
    title: str
    description: str
    background_color: str
    image: IResource
    price: float
    is_sold_out: bool
    type: str


ShopFreezed = dict[str, list[ShopProductFreezed]]


class ShopProduct(ABC):
    """
    各种商店的商品的元类
    """

    @abstractmethod
    async def title(self, uow: UnitOfWork, uid: int) -> str:
        """商品的标题"""

    @abstractmethod
    async def description(self, uow: UnitOfWork, uid: int) -> str:
        """商品的描述"""

    @abstractmethod
    async def background_color(self, uow: UnitOfWork, uid: int) -> str:
        """商品的背景颜色"""

    @abstractmethod
    async def price(self, uow: UnitOfWork, uid: int) -> float:
        """商品的价格"""

    @abstractmethod
    async def is_sold_out(self, uow: UnitOfWork, uid: int) -> bool:
        """判断一个商品是否被卖光"""

    @abstractmethod
    def match(self, name: str) -> bool:
        """判断用户输入的名字是否符合这个产品"""

    @abstractmethod
    async def gain(self, uow: UnitOfWork, uid: int):
        """成功购买一个商品时触发的操作"""

    @abstractmethod
    async def image(self, uow: UnitOfWork, uid: int) -> IResource:
        """商品的图片"""

    @property
    @abstractmethod
    def type(self) -> str:
        """商品的类型"""

    async def freeze(self, uow: UnitOfWork, uid: int) -> ShopProductFreezed:
        return ShopProductFreezed(
            title=await self.title(uow, uid),
            description=await self.description(uow, uid),
            background_color=await self.background_color(uow, uid),
            image=await self.image(uow, uid),
            price=await self.price(uow, uid),
            is_sold_out=await self.is_sold_out(uow, uid),
            type=self.type,
        )


class SkinProduct(ShopProduct):
    @property
    def type(self):
        return "皮肤"

    async def title(self, uow: UnitOfWork, uid: int):
        return "皮肤" + self._title

    async def image(self, uow: UnitOfWork, uid: int):
        return KagamiResourceManagers.xiaoge_blurred(f"sid_{self.sid}.png")

    async def description(self, uow: UnitOfWork, uid: int):
        return f"{self._aname}的皮肤"

    async def background_color(self, uow: UnitOfWork, uid: int):
        return self._bgc

    async def price(self, uow: UnitOfWork, uid: int):
        return self._price

    async def is_sold_out(self, uow: UnitOfWork, uid: int) -> bool:
        return await uow.skin_inventory.do_user_have(uid, self.sid)

    def match(self, name: str) -> bool:
        return name in (self._title, "皮肤" + self._title)

    async def gain(self, uow: UnitOfWork, uid: int):
        await uow.skin_inventory.give(uid, self.sid)

    def __init__(
        self, sid: int, name: str, aname: str, price: float, bgc: str
    ) -> None:
        self.sid = sid
        self._title = name
        self._aname = aname
        self._bgc = bgc
        self._price = price


class AddSlots(ShopProduct):
    @property
    def type(self):
        return "道具"

    async def _slots(self, uow: UnitOfWork, uid: int) -> int:
        return (await uow.user_catch_time.get_user_time(uid)).slot_count

    async def title(self, uow: UnitOfWork, uid: int):
        return "增加卡槽上限"

    async def description(self, uow: UnitOfWork, uid: int) -> str:
        return f"增加卡槽上限至{await self._slots(uow, uid) + 1}"

    async def image(self, uow: UnitOfWork, uid: int):
        return KagamiResourceManagers.res("add1.png")

    async def price(self, uow: UnitOfWork, uid: int) -> float:
        return 25 * (2 ** (await self._slots(uow, uid)))

    async def is_sold_out(self, uow: UnitOfWork, uid: int) -> bool:
        return False

    async def background_color(self, uow: UnitOfWork, uid: int):
        return "#97DD80"

    def match(self, name: str) -> bool:
        return name in ["加上限", "增加上限", "增加卡槽上限"]

    async def gain(self, uow: UnitOfWork, uid: int):
        await uow.users.add_slot_count(uid, 1)


class MergeMachine(ShopProduct):
    @property
    def type(self):
        return "道具"

    async def title(self, uow: UnitOfWork, uid: int):
        return "小哥合成凭证"

    async def description(self, uow: UnitOfWork, uid: int):
        return "购买合成小哥机器的使用权"

    async def background_color(self, uow: UnitOfWork, uid: int):
        return "#9E9D95"

    async def price(self, uow: UnitOfWork, uid: int):
        return 1200

    async def image(self, uow: UnitOfWork, uid: int):
        return KagamiResourceManagers.res("merge_machine.png")

    async def is_sold_out(self, uow: UnitOfWork, uid: int) -> bool:
        return await uow.user_flag.have(uid, "合成")

    def match(self, name: str) -> bool:
        return name in ["小哥合成凭证", "合成小哥凭证", "合成凭证", "合成"]

    async def gain(self, uow: UnitOfWork, uid: int):
        await uow.user_flag.add(uid, "合成")


# class SignHint(ShopProduct):
#     @property
#     def type(self):
#         return "道具"

#     async def title(self, uow: UnitOfWork, uid: int) -> str:
#         return "签到提醒"

#     async def description(self, uow: UnitOfWork, uid: int) -> str:
#         return "小镜会在合适的时候提醒你记得签到的，如果她还能找得到你"

#     async def background_color(self, uow: UnitOfWork, uid: int):
#         return "#9e9d95"

#     async def price(self, uow: UnitOfWork, uid: int):
#         return 800

#     async def


class ShopService:
    products: dict[str, list[ShopProduct]]

    def __init__(self) -> None:
        self.products = {}

    def register(self, product: ShopProduct):
        self.products.setdefault(product.type, [])
        self.products[product.type].append(product)

    def get(self, name: str) -> ShopProduct | None:
        for ls in self.products.values():
            for p in ls:
                if p.match(name):
                    return p

        return None

    def __getitem__(self, name: str) -> ShopProduct:
        p = self.get(name)
        if p is None:
            raise ObjectNotFoundException("商品")
        return p

    async def freeze(self, uow: UnitOfWork, uid: int) -> ShopFreezed:
        result: ShopFreezed = {}
        for key, items in self.products.items():
            result[key] = [await i.freeze(uow, uid) for i in items]
        return result


async def build_xjshop(uow: UnitOfWork) -> ShopService:
    service = ShopService()

    # 注册道具
    service.register(MergeMachine())
    service.register(AddSlots())
    # service.register(SignHint())

    # 注册皮肤信息
    for sid, aid, sname, _, price in await uow.skins.all():
        if price <= 0:
            continue
        info = await uow.awards.get_info(aid)
        service.register(SkinProduct(sid, sname, info.name, price, info.color))

    return service

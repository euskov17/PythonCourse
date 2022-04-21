from dataclasses import dataclass, field, InitVar
from abc import ABC


DISCOUNT_PERCENTS = 15


class Item:
    # note: mind the order of fields (!)
    cost: int
    title: str
    item_id: int


# Do not remove `# type: ignore`
# It is [a really old issue](https://github.com/python/mypy/issues/5374)
@dataclass  # type: ignore
class Position(ABC):
    item: Item

    def cost(self):
        pass


class CountedPosition(Position):
    count: int


class WeightedPosition(Position):
    weight: float


class Order:
    order_id: int
    positions: list[Position]
    cost: int
    have_promo: bool

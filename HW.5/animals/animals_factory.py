import typing as tp

from abc import abstractmethod, ABC
from .animals import Cat, Cow, Dog


class Animal(ABC):
    @abstractmethod
    def say(self):
        pass


class CatAdapter(Animal):
    def say(self):
        return "meow"


class DogAdapter(Animal):
    def say(self):
        return "woof"


class CowAdapter(Animal):
    def say(self):
        return "moo"


def animals_factory(animal: tp.Any) -> Animal:
    if isinstance(animal, Cat):
        return CatAdapter()
    elif isinstance(animal, Dog):
        return DogAdapter()
    elif isinstance(animal, Cow):
        return CowAdapter()
    raise TypeError

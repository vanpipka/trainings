from abc import ABCMeta, abstractmethod
import random
from typing import Type


class IEngine(metaclass=ABCMeta):

    def __init__(self, name) -> None:
        self.name = name

    @abstractmethod
    def power(self) -> None:
        pass

    def __str__(self) -> str:
        pass


class JapaneseEngine(IEngine):

    def power(self) -> None:
        print("360")

    def __str__(self) -> str:
        return self.name

    def kek(self):
        print("lol")


class AmericanEngine(IEngine):
    def power(self) -> None:
        print("320")

    def __str__(self) -> str:
        return self.name


class Factory:

    def __init__(self, engine_factory: Type[IEngine]) -> None:
        self.engine_factory = engine_factory

    def make_engine(self, name: str) -> IEngine:

        engine = self.engine_factory(name)
        print(f"made {engine}")
        return engine


# Create a random engine
def random_engine(name: str) -> IEngine:
    return random.choice([JapaneseEngine, AmericanEngine])(name)


if __name__ == "__main__":

    # fixed
    j_engine = Factory(JapaneseEngine).make_engine("GRT")
    j_engine.power()

    # random_engine
    factory = Factory(random_engine)

    for i in ["x1", "x2", "x3", "x4"]:
        print("="*20)
        engine = factory.make_engine(i)
        engine.power()

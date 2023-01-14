from __future__ import annotations

import copy
from typing import Any


class Prototype:
    def __init__(self, value: str = "default", **attrs: Any) -> None:
        self.value = value
        self.__dict__.update(attrs)

    def clone(self, **attrs: Any) -> Prototype:
        obj = copy.deepcopy(self)
        obj.__dict__.update(attrs)
        return obj


class PrototypeDispatcher:
    def __init__(self):
        self._objects = {}

    def get_objects(self) -> dict[str, Prototype]:
        return self._objects

    def register_object(self, name: str, obj: Prototype) -> None:
        self._objects[name] = obj

    def unregister_object(self, name: str) -> None:
        del self._objects[name]


def main() -> None:

    dispatcher = PrototypeDispatcher()
    prototype = Prototype()
    d = prototype.clone()
    a = prototype.clone(value='a-value', category='a')
    b = a.clone(value='b-value', is_checked=True)
    dispatcher.register_object('objecta', a)
    dispatcher.register_object('objectb', b)
    dispatcher.register_object('default', d)
    for n, p in dispatcher.get_objects().items():
         print({n: p.value})

    print(b.category, b.is_checked)


if __name__ == "__main__":
    main()

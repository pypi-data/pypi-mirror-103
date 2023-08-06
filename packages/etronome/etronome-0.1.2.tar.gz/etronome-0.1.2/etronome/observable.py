from typing import Callable, Generic, Protocol, TypeVar

T = TypeVar('T')
S = TypeVar('S', contravariant=True)


class Observer(Protocol[S]):
    def update_(self, value: S) -> None:
        ...


class Observable(Generic[T]):
    def __init__(
        self,
        observers: str,
        transformer: Callable[[T], T] = lambda x: x
    ) -> None:
        self.observers = observers
        self._transformer = transformer

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

    def __set__(self, instance: object, value: T) -> None:
        transformed = self._transformer(value)
        instance.__dict__[self.name] = transformed
        observers = instance.__dict__[self.observers]
        for observer in observers:
            observer.update_(transformed)

    def __get__(self, instance: object, owner: type = None) -> T:
        return instance.__dict__[self.name]

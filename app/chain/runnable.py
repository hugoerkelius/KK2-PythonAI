from abc import ABC, abstractmethod
from typing import Any, Callable, Generic, TypeVar

I = TypeVar("I")
O = TypeVar("O")
N = TypeVar("N")


class Runnable(Generic[I, O], ABC):
    @abstractmethod
    def run(self, input: I) -> O:
        ...

    def __or__(self, other: "Runnable[O, N] | Callable") -> "RunnableSequence[I, N]":
        if isinstance(other, Runnable):
            return RunnableSequence(self, other)
        if callable(other):
            return RunnableSequence(self, RunnableLambda(other))
        return NotImplemented

    def __ror__(self, other: Callable[[Any], I]) -> "RunnableSequence[Any, O]":
        return RunnableSequence(RunnableLambda(other), self)


class RunnableLambda(Runnable[I, O]):
    def __init__(self, func: Callable[[I], O]) -> None:
        self._func = func

    def run(self, input: I) -> O:
        return self._func(input)


class RunnableSequence(Runnable[I, O]):
    def __init__(self, first: Runnable[I, Any], second: Runnable[Any, O]) -> None:
        self._first = first
        self._second = second

    def run(self, input: I) -> O:
        intermediate = self._first.run(input)
        return self._second.run(intermediate)
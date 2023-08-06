from __future__ import annotations

import abc
import typing

from lime_uow import resource

__all__ = ("Repository",)


E = typing.TypeVar("E")


class Repository(
    resource.Resource["Repository[E]"],
    abc.ABC,
    typing.Generic[E],
):
    """Interface to access elements of a collection"""

    @abc.abstractmethod
    def add(self, /, item: E) -> E:
        raise NotImplementedError

    @abc.abstractmethod
    def add_all(self, /, items: typing.Collection[E]) -> typing.Collection[E]:
        raise NotImplementedError

    @abc.abstractmethod
    def all(self) -> typing.Iterable[E]:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, /, item: E) -> E:
        raise NotImplementedError

    @abc.abstractmethod
    def delete_all(self) -> None:
        raise NotImplementedError

    def open(self) -> Repository[E]:
        return self

    @abc.abstractmethod
    def set_all(self, /, items: typing.Collection[E]) -> typing.Collection[E]:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, /, item: E) -> E:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, /, item_id: typing.Any) -> E:
        raise NotImplementedError

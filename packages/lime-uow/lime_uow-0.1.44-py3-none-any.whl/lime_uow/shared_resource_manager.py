from __future__ import annotations

import types
import typing

from lime_uow import exceptions, resource

__all__ = (
    "SharedResourceManager",
    "PlaceholderSharedResourceManager",
)

T = typing.TypeVar("T")


class SharedResourceManager:
    """
    SharedResources manages resources that live for the duration of the process.
    """

    def __init__(self, /, *shared_resource: resource.Resource[typing.Any]):
        resource.check_for_ambiguous_implementations(shared_resource)

        self.__shared_resources: typing.Dict[str, resource.Resource[typing.Any]] = {
            r.interface().__name__: r for r in shared_resource
        }
        # self.__shared_resources = tuple(shared_resource)
        self.__handles: typing.Dict[str, typing.Any] = {}
        self.__opened = False
        self.__closed = False

    def __enter__(self) -> SharedResourceManager:
        if self.__opened:
            raise exceptions.ResourcesAlreadyOpen()
        if self.__closed:
            raise exceptions.ResourceClosed()
        self.__opened = True
        return self

    def __exit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_val: typing.Optional[BaseException],
        exc_tb: typing.Optional[types.TracebackType],
    ) -> typing.Literal[False]:
        self.close()
        return False

    def close(self):
        if self.__closed:
            raise exceptions.ResourceClosed()
        for resource_name in self.__handles.keys():
            self.__shared_resources[resource_name].close()
        self.__handles = {}
        self.__closed = True
        self.__opened = False

    def exists(self, /, resource_type: typing.Type[resource.Resource[T]]) -> bool:
        return resource_type.__name__ in self.__shared_resources.keys()

    def get(
        self,
        resource_type: typing.Type[resource.Resource[T]],
    ) -> T:
        if self.__closed:
            raise exceptions.ResourceClosed()
        elif (
            interface_name := resource_type.interface().__name__
        ) in self.__handles.keys():
            return self.__handles[interface_name]
        elif interface_name in self.__shared_resources.keys():
            r = self.__shared_resources[interface_name]
            handle = r.open()
            self.__handles[interface_name] = handle
            return handle
        else:
            raise exceptions.MissingResourceError(
                resource_name=interface_name,
                available_resources=self.__shared_resources.keys(),
            )

    def __eq__(self, other: object) -> bool:
        if other.__class__ is self.__class__:
            # noinspection PyTypeChecker
            return (
                self.__shared_resources.keys()
                == typing.cast(SharedResourceManager, other).__shared_resources.keys()
            )
        else:
            return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__shared_resources)

    def __repr__(self) -> str:
        resources_str = ", ".join(self.__shared_resources.keys())
        return f"{self.__class__.__name__}: {resources_str}"


class PlaceholderSharedResourceManager(SharedResourceManager):
    def __init__(self):
        super().__init__()

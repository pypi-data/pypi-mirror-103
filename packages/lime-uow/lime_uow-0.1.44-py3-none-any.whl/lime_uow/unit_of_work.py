from __future__ import annotations

import abc
import typing

from lime_uow import exceptions, resource, shared_resource_manager

__all__ = (
    "PlaceholderUnitOfWork",
    "UnitOfWork",
)

# noinspection PyTypeChecker
T = typing.TypeVar("T", bound="UnitOfWork")


class UnitOfWork(abc.ABC):
    def __init__(self):
        self.__resources: typing.Optional[
            typing.Dict[str, resource.Resource[typing.Any]]
        ] = None
        self.__resources_validated = False
        self.__shared_resource_manager: typing.Optional[
            shared_resource_manager.SharedResourceManager
        ] = None

    def __enter__(self: T) -> T:
        if self.__shared_resource_manager is None:
            shared_resources = self.create_shared_resources()
            self.__shared_resource_manager = (
                shared_resource_manager.SharedResourceManager(*shared_resources)
            )
        fresh_resources = self.create_resources(self.__shared_resource_manager)
        resource.check_for_ambiguous_implementations(fresh_resources)
        self.__resources = {r.interface().__name__: r for r in fresh_resources}
        self.__resources_validated = True
        return self

    def __exit__(self, *args) -> typing.Literal[False]:
        errors: typing.List[exceptions.RollbackError] = []
        try:
            self.rollback()
        except exceptions.RollbackErrors as e:
            errors += e.rollback_errors
        self.__resources = None
        if errors:
            raise exceptions.RollbackErrors(*errors)
        return False

    def close(self) -> None:
        if self.__shared_resource_manager:
            self.__shared_resource_manager.close()

    def exists(
        self, /, resource_type: typing.Type[resource.Resource[typing.Any]]
    ) -> bool:
        if self.__resources is None:
            raise exceptions.OutsideTransactionError()
        else:
            return resource_type.__name__ in self.__resources.keys()

    def get(self, /, resource_type: typing.Type[resource.Resource[T]]) -> T:
        if self.__resources is None:
            raise exceptions.OutsideTransactionError()
        else:
            if self.__shared_resource_manager is None:
                raise exceptions.OutsideTransactionError()
            elif self.__shared_resource_manager.exists(resource_type):
                return self.__shared_resource_manager.get(resource_type)
            elif (interface_name := resource_type.__name__) in self.__resources.keys():
                return self.__resources[interface_name].open()
            else:
                raise exceptions.MissingResourceError(
                    resource_name=interface_name,
                    available_resources=self.__resources.keys(),
                )

    @abc.abstractmethod
    def create_resources(
        self, /, shared_resources: shared_resource_manager.SharedResourceManager
    ) -> typing.Iterable[resource.Resource[typing.Any]]:
        raise NotImplementedError

    @abc.abstractmethod
    def create_shared_resources(
        self,
    ) -> typing.Iterable[resource.Resource[typing.Any]]:
        raise NotImplementedError

    def rollback(self):
        errors: typing.List[exceptions.RollbackError] = []
        if self.__resources is None:
            raise exceptions.OutsideTransactionError()
        else:
            for r in self.__resources.values():
                try:
                    r.rollback()
                except Exception as e:
                    errors.append(
                        exceptions.RollbackError(
                            f"An error occurred while rolling back {self.__class__.__name__}: {e}",
                        )
                    )

        if errors:
            raise exceptions.RollbackErrors(*errors)

    def save(self):
        # noinspection PyBroadException
        try:
            if self.__resources is None:
                raise exceptions.OutsideTransactionError()
            else:
                for r in self.__resources.values():
                    r.save()
        except:
            self.rollback()
            raise


class PlaceholderUnitOfWork(UnitOfWork):
    def __init__(self):
        super().__init__()

    def create_resources(
        self, shared_resources: shared_resource_manager.SharedResourceManager
    ) -> typing.List[resource.Resource[typing.Any]]:
        return []

    def create_shared_resources(self) -> typing.List[resource.Resource[typing.Any]]:
        return []

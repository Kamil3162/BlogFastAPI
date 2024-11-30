from typing import TypeVar, Type, Dict
from sqlalchemy.orm import Session
from fastapi import Depends
from ..utils.utils import get_db


# Service part of code to get service instance during perform a request
ServiceType = TypeVar("ServiceType")

class ServiceFactory:
    _instances: Dict[Type, object] = {}

    @classmethod
    def get_instance(
        cls,
        service_class: Type[ServiceType],
        db: Session
    ) -> ServiceType:
        if service_class not in cls._instances:
            cls._instances[service_class] = service_class(db)
        else:
            cls._instances[service_class]._db = db

        return cls._instances[service_class]

    @classmethod
    def get_redis_instance(
        cls,
        service_class: Type[ServiceType],
    ) -> ServiceType:
        if service_class not in cls._instances:
            cls._instances[service_class] = service_class()
        return cls._instances[service_class]

    @classmethod
    def swap_instance(
        cls,
        service_class: Type[ServiceType],
        db: Session
    ) -> ServiceType:
        try:
            service_instance = service_class(db)
            cls._instances.pop(service_class)
            cls._instances[service_class] = service_instance
            return
        except KeyError:
            raise KeyError("You pass invalid instance key")

    @classmethod
    def clear_instance(cls):
        cls._instances.clear()


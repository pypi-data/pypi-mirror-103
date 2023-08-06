from abc import ABC, abstractmethod


class Provider(ABC):

    @classmethod
    @abstractmethod
    def get_provider_key(cls) -> str:
        pass

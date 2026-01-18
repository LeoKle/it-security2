from abc import ABC, abstractmethod

from interfaces.server_interface import ServerInterface


class PersonInterface(ABC):
    @abstractmethod
    def publish_prekeys(self, server: ServerInterface): ...

    @abstractmethod
    def receive_x3dh(self, server: ServerInterface): ...

    @abstractmethod
    def initiate_x3dh(self, peer_name: str, server: ServerInterface): ...

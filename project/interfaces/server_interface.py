from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class KeyBundle:
    identity_key: str
    signed_prekey: str
    onetime_prekey: str


class ServerInterface(ABC):
    @abstractmethod
    def publish_prekeys(self, name: str, bundle: KeyBundle): ...

    @abstractmethod
    def fetch_prekeys(self, name: str) -> KeyBundle | None: ...

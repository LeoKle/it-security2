from abc import ABC, abstractmethod


class CryptoInterface(ABC):
    @abstractmethod
    def generate_keypair(self): ...

    @abstractmethod
    def dh(self, private_key, public_key) -> bytes: ...

    @abstractmethod
    def kdf(self, *secrets: bytes) -> bytes: ...

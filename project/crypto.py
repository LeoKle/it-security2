import hashlib
import os

from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

from interfaces.crypto_interface import CryptoInterface


class SimpleCrypto(CryptoInterface):
    def generate_keypair(self):
        key = os.urandom(32)
        return key, key  # no distinction in this simple implementation

    def dh(self, private_key, public_key):
        return hashlib.sha256(b"".join(sorted([private_key, public_key]))).digest()

    def kdf(self, *secrets):
        h = hashlib.sha256()
        for s in secrets:
            h.update(s)
        return h.digest()


class RealCrypto(CryptoInterface):
    def generate_keypair(self):
        private = x25519.X25519PrivateKey.generate()
        public = private.public_key()
        return private, public

    def dh(self, private_key, public_key):
        return private_key.exchange(public_key)

    def kdf(self, *secrets):
        material = b"".join(secrets)
        return HKDF(
            algorithm=hashes.SHA256(), length=32, salt=None, info="X3DH Demo"
        ).derive(material)

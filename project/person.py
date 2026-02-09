from crypto import SimpleCrypto
from interfaces.crypto_interface import CryptoInterface
from interfaces.person_interface import PersonInterface
from interfaces.server_interface import KeyBundle, Message, ServerInterface


class Person(PersonInterface):
    def __init__(self, name, crypto: CryptoInterface = None):
        if not crypto:
            crypto = SimpleCrypto()

        self.name = name
        self.crypto = crypto

        self.IK_priv, self.IK_pub = self.crypto.generate_keypair()
        # used when responding
        self.SPK_priv, self.SPK_pub = self.crypto.generate_keypair()
        self.OPK_priv, self.OPK_pub = self.crypto.generate_keypair()

        self.shared_secret = None

    def publish_prekeys(self, server):
        key_bundle = KeyBundle(
            identity_key=self.IK_pub,
            signed_prekey=self.SPK_pub,
            onetime_prekey=self.OPK_pub,
        )
        server.publish_prekeys(self.name, key_bundle)

    def receive_x3dh(self, server: ServerInterface):
        message: Message = server.fetch_message(self.name)

        if not message:
            print(
                f"{self.name} fetched his messages, but no party tried to initiate a conversation with him"
            )
            return

        DH1 = self.crypto.dh(self.SPK_priv, message.identity_key)
        DH2 = self.crypto.dh(self.IK_priv, message.ephemeral_key)
        DH3 = self.crypto.dh(self.SPK_priv, message.ephemeral_key)
        DH4 = self.crypto.dh(self.OPK_priv, message.ephemeral_key)

        self.shared_secret = self.crypto.kdf(DH1, DH2, DH3, DH4)
        print(f"{self.name}: computed shared secret {self.shared_secret}")

    def initiate_x3dh(self, peer_name: str, server: ServerInterface):
        peer_bundle = server.fetch_prekeys(peer_name)

        if not peer_bundle:
            print(
                f"{self.name} tried to start communication with peer {peer_name} but peer has not submitted keys"
            )
            return

        EK_priv, EK_pub = self.crypto.generate_keypair()

        DH1 = self.crypto.dh(self.IK_priv, peer_bundle.signed_prekey)
        DH2 = self.crypto.dh(EK_priv, peer_bundle.identity_key)
        DH3 = self.crypto.dh(EK_priv, peer_bundle.signed_prekey)
        DH4 = self.crypto.dh(EK_priv, peer_bundle.onetime_prekey)

        self.shared_secret = self.crypto.kdf(DH1, DH2, DH3, DH4)

        print(f"{self.name}: computed shared secret {self.shared_secret}")

        server.post_message(peer_name, Message(self.IK_pub, EK_pub))

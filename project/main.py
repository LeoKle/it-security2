from crypto import RealCrypto
from person import Person
from server import Server

if __name__ == "__main__":
    crypto = RealCrypto()
    server = Server()

    alice = Person("alice", crypto=crypto)
    bob = Person("bob", crypto=crypto)

    bob.publish_prekeys(server)

    alice.initiate_x3dh("bob", server)
    bob.receive_x3dh(server)

    if (
        alice.shared_secret == bob.shared_secret
        and alice.shared_secret
        and bob.shared_secret
    ):
        print("Shared secret established")

from interfaces.server_interface import KeyBundle, ServerInterface


class Server(ServerInterface):
    def __init__(self):
        self.prekey_bundles = {}

    def publish_prekeys(self, name: str, bundle: KeyBundle):
        self.prekey_bundles[name] = bundle

    def fetch_prekeys(self, name: str) -> KeyBundle | None:
        return self.prekey_bundles.get(name)

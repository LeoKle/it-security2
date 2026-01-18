from interfaces.server_interface import KeyBundle, Message, ServerInterface


class Server(ServerInterface):
    def __init__(self):
        self.prekey_bundles = {}
        self.messages = {}

    def publish_prekeys(self, name: str, bundle: KeyBundle):
        self.prekey_bundles[name] = bundle

    def fetch_prekeys(self, name: str) -> KeyBundle | None:
        return self.prekey_bundles.get(name)

    def fetch_message(self, name: str) -> Message | None:
        return self.messages.get(name)

    def post_message(self, recipient: str, message: Message):
        self.messages[recipient] = message

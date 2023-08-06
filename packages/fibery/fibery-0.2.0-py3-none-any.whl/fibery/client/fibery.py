from fibery.client.base import Client
from fibery.client.schema import Schema
from fibery.client.webhook import WebHook


class Fibery:

    client: Client = None
    webhook: WebHook = WebHook()
    schema: Schema = Schema()

    def __init__(self, client: Client):
        self.client = client

    def get_resources(self):
        return [c for c in dir(self) if isinstance(getattr(self, c), WebHook)]

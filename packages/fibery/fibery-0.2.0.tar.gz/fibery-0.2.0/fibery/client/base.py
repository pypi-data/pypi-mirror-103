import functools
import requests

from typing import TYPE_CHECKING, Literal, Dict, Any, List, Union
from pydantic import BaseModel

from fibery.conf import settings

if TYPE_CHECKING:
    from fibery.client.fibery import Fibery


class ArgsDescriptor:
    pass


class FiberyApiError(Exception):
    pass


class ManyResult(BaseModel):
    __root__: List


class BaseClient:

    workspace: str
    endpoint: str

    def __init__(self, token, workspace, endpoint="https://{workspace}.fibery.io/api/"):
        self.endpoint = endpoint.format(workspace=workspace)
        self.workspace = workspace
        self.token = token

    def request(self, method: Literal["GET", "POST", "PUT", "DELETE"],
                resource, json: dict = None, data: str = None, coerce_to: BaseModel = None, many=False):
        headers = {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        url = "/".join([self.endpoint.strip("/"), resource])
        response = requests.request(method, url, json=json, data=data, headers=headers)
        if response.status_code != 200:
            raise FiberyApiError(f"Error {response.status_code}: {response.content}")

        result = response.json()
        if coerce_to:
            if many:
                result = ManyResult(__root__=[coerce_to.parse_obj(obj) for obj in result])
            else:
                result = coerce_to.parse_obj(result)
        return result

    def get(self, *args, **kwargs):
        return self.request("GET", *args, **kwargs)

    def update(self, *args, **kwargs):
        return self.request("PUT", *args, **kwargs)

    def create(self, *args, **kwargs):
        return self.request("POST", *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.request("DELETE", *args, **kwargs)

    def command(self, command, args=None):
        payload = {
            "command": command
        }
        if args:
            payload.update({
                "args": args
            })

        result = self.request("POST", "commands", json=[payload])[0]
        success = result["success"]
        result = result["result"]
        if not success:
            raise FiberyApiError(result)
        return result


class Client(BaseClient):
    pass


def default_client():
    return Client(
        token=settings.api_token.get_secret_value(),
        workspace=settings.workspace
    )


class BaseResource:

    fibery: "Fibery" = None
    name: str = None

    def init(self, fibery: "Fibery"):
        self.fibery = fibery

    def __get__(self, instance, owner):
        if not instance:
            raise TypeError("Forbidden to call resource from Fibery class, use Fiber() instance instead. "
                            "Example: Fiber(...).resource")
        if not self.fibery:
            self.fibery = instance
        return self

    @property
    def client(self):
        return self.fibery.client

    def get_methods(self):
        result = []
        for c in dir(self):
            member = getattr(self, c)
            if not callable(member):
                continue
            if c in {"init", "get_methods"}:
                continue
            if c.startswith("_"):
                continue
            result.append(c)

        return result

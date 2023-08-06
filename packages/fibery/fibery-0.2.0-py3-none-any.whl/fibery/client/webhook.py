from typing import List

from pydantic import BaseModel, AnyUrl

from fibery.client.base import BaseResource
from fibery.models import FiberyType


class AddResult(BaseModel):
    id: int
    url: AnyUrl
    type: FiberyType
    state: str
    runs: List = []


class GetResult(AddResult):
    pass


class WebHook(BaseResource):

    name = "webhooks/v2"

    def create(self, url: str, type: FiberyType) -> AddResult:
        return self.client.create(self.name, json={
            "url": url,
            "type": type
        }, coerce_to=AddResult)

    def list(self) -> List[GetResult]:
        return self.client.get(self.name, coerce_to=GetResult, many=True)

    def delete(self, pk) -> bool:
        name = f"{self.name}/{pk}"
        return self.client.delete(name)

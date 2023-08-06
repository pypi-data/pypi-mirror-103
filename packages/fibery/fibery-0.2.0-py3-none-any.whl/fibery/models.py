from typing import Literal, Dict, List, Any

from pydantic import BaseModel


FiberyType = str


class BaseEffect(BaseModel):
    id: str
    type: FiberyType


class FiberyEntityCreateEffect(BaseEffect):
    effect: Literal["fibery.entity/update"] = "fibery.entity/create"
    values: Dict[str, Any]


class FiberyEntityUpdateEffect(BaseEffect):
    effect: Literal["fibery.entity/update"] = "fibery.entity/update"
    values: Dict[str, Any]
    valuesBefore: Dict[str, Any]


class FiberyEntityDeleteEffect(BaseEffect):
    effect: Literal["fibery.entity/update"] = "fibery.entity/delete"
    valuesBefore: Dict[str, Any]


class FiberyAddCollectionItemsEffect(BaseEffect):
    effect: Literal["fibery.entity/add-collection-items"] = "fibery.entity/add-collection-items"
    field: str
    items: List[Dict[str, Any]]


class FiberyRemoveCollectionItemsEffect(BaseEffect):
    effect: Literal["fibery.entity/add-collection-items"] = "fibery.entity/remove-collection-items"
    field: str
    items: List[Dict[str, Any]]

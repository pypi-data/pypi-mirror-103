from enum import Enum
from typing import List, Union, Any, Dict, Literal

from pydantic import BaseModel, AnyUrl, Field, SecretStr
from pydantic.typing import ForwardRef

from fibery.client.base import BaseResource
from fibery.models import FiberyType


class QueryResult:
    pass


class Expression(BaseModel):
    pass


class Operator(str, Enum):
    EQ = "="
    NEQ = "!="
    LT = "<"
    LTE = "<="
    GT = ">"
    GTE = ">="
    CONTAINS = "q/contains"
    NCONTAINS = "q/not-contains"
    IN = "q/in"
    NIN = "q/not-in"
    AND = "q/and"
    OR = "q/or"


def field(*path):
    return path


def eq(lft, rgt):
    return Operator.EQ, lft, rgt


def neq(lft, rgt):
    return Operator.NEQ, lft, rgt


def lt(lft, rgt):
    return Operator.LT, lft, rgt


def lte(lft, rgt):
    return Operator.LTE, lft, rgt


def gt(lft, rgt):
    return Operator.GTE, lft, rgt


def gte(lft, rgt):
    return Operator.GTE, lft, rgt


def contains(lft, rgt):
    return Operator.CONTAINS, lft, rgt


def ncontains(lft, rgt):
    return Operator.NCONTAINS, lft, rgt


def In(lft, rgt):
    return Operator.IN, lft, rgt


def nin(lft, rgt):
    return Operator.NEQ, lft, rgt


class Query(BaseModel):
    type: FiberyType = Field(alias="q/from")
    select: List[Union[str, "Query"]] = Field(alias="q/select")
    where: List[Expression] = Field(alias="q/where")
    order: List[Union[str, "Query"]] = Field(alias="q/order-by")
    limit: List[Union[str, "Query"]] = Field(alias="q/limit")


Query.update_forward_refs()


class WebHook(BaseResource):

    name = "fibery.entity/query2"

    def query(self, query: Query, **params) -> QueryResult:
        return self.client.command(self.name, args={
            "query": query.dict()
        })


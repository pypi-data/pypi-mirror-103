import re
from typing import Optional, Dict, List

import typer
import functools

from click import BadArgumentUsage
from pydantic import constr
from typer import Option

from fibery.client.base import default_client
from fibery.client.fibery import Fibery
from fibery.conf import settings
from fibery.console.commands.base import output
from fibery.enums import FormatEnum


api = typer.Typer()


def init_fibery(f):
    @functools.wraps(f)
    def wrapper(resource, method, arg: List[str], *args, **kwargs):
        fibery = Fibery(
            client=default_client()
        )

        try:
            resource = getattr(fibery, resource)
        except AttributeError:
            choices = fibery.get_resources()
            raise BadArgumentUsage(
                f"Fibery '{resource}' resource type does not exist, choices are {', '.join(choices)}")

        try:
            method = getattr(resource, method)
        except AttributeError:
            choices = resource.get_methods()
            raise BadArgumentUsage(f"Resource '{method}' method does not exist, choices are {', '.join(choices)}")

        call_args = dict()
        for a in arg:
            if a.count("=") != 1:
                raise BadArgumentUsage(f"Arg value should be in format key=value")
            key, value = a.split("=")
            call_args.update({
                key: value
            })

        return f(resource, method, call_args, *args, **kwargs)

    return wrapper


KEY_VALUE_PATTERN = r'[^=]+\=.+'


@api.command(name="call")
@init_fibery
def call(resource: str,
         method: str,
         arg: List[str] = None,
         format: FormatEnum = FormatEnum.json):
    settings.output_format = format
    output(method(**arg))

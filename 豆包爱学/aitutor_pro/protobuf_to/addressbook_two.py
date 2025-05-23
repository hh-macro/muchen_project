# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: addressbook_two.proto
# plugin: python-betterproto
from dataclasses import dataclass
from typing import List

import betterproto


@dataclass
class GetByUserInitTwo(betterproto.Message):
    name: int = betterproto.int32_field(1)
    eutex_a: int = betterproto.int32_field(2)
    content: int = betterproto.int32_field(3)
    build: str = betterproto.string_field(4)
    device: int = betterproto.int32_field(5)
    inner_list: List["InnerMessage"] = betterproto.message_field(6)


@dataclass
class InnerMessage(betterproto.Message):
    nested: "NestedMessage" = betterproto.message_field(301)


@dataclass
class NestedMessage(betterproto.Message):
    """定义更深层的消息"""

    deep_nested: List["DeepNestedMessage"] = betterproto.message_field(1)


@dataclass
class DeepNestedMessage(betterproto.Message):
    """定义最深层的消息"""

    card_stem: str = betterproto.string_field(8)
    prompt_content: List["CoreNestedMessage"] = betterproto.message_field(9)


@dataclass
class CoreNestedMessage(betterproto.Message):
    con_text: str = betterproto.string_field(2)

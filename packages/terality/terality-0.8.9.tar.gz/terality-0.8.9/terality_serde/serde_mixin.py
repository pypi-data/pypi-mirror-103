import base64
import inspect
import zlib
from dataclasses import dataclass, field
import json
from functools import cached_property, lru_cache
from typing import Any, ClassVar, Dict, List, Type

from . import ExternalTypeSerializer


class SerdeMixin:
    @property
    def class_name(self) -> str:
        return self.__class__.__name__

    @classmethod
    @lru_cache
    def cached_properties_names(cls):
        return {k for k, v in inspect.getmembers(cls) if isinstance(v, cached_property)}

    @property
    def dict(self) -> dict:
        dict_ = {k: v for k, v in self.__dict__.items() if k not in self.__class__.cached_properties_names()}
        return dict_

    @classmethod
    def from_dict(cls, **kwargs):
        return cls(**kwargs)


@dataclass
class SerdeConfig:
    _internal_type_attribute: ClassVar[str] = '!terality:internal_type'
    _external_type_attribute: ClassVar[str] = '!terality:external_type'
    _internal_types_mapping: List[Type[SerdeMixin]]
    _external_types_serializer: List[ExternalTypeSerializer]
    _internal_types: Dict[str, SerdeMixin] = field(init=False)
    _external_types: Dict[Type, ExternalTypeSerializer] = field(init=False)
    _external_types_serde: Dict[str, ExternalTypeSerializer] = field(init=False)

    def __post_init__(self):
        self._internal_types = {internal.__name__: internal for internal in self._internal_types_mapping}
        self._external_types = {ex.class_: ex for ex in self._external_types_serializer}
        self._external_types_serde = {ex.class_name: ex for ex in self._external_types_serializer}

    def serialize(self, o):
        if isinstance(o, SerdeMixin):
            dict_ = o.dict
            dict_[self._internal_type_attribute] = o.class_name
            encoded = dict_
        elif type(o) in self._external_types:
            external_type = self._external_types[type(o)]
            dict_ = external_type.to_json(o)
            dict_[self._external_type_attribute] = external_type.class_name
            encoded = dict_
        else:
            encoded = o
        if isinstance(encoded, list):
            return [self.serialize(elt) for elt in encoded]
        elif isinstance(encoded, dict):
            return {self.serialize(k): self.serialize(v) for k, v in encoded.items()}
        else:
            return encoded

    def deserialize(self, obj):
        if self._internal_type_attribute in obj:
            internal_type_name = obj.pop(self._internal_type_attribute)
            internal_type = self._internal_types[internal_type_name]
            return internal_type.from_dict(**obj)
        if self._external_type_attribute in obj:
            external_type_name = obj.pop(self._external_type_attribute)
            deserializer = self._external_types_serde[external_type_name]
            return deserializer.from_json(**obj)
        return obj


def loads(s: str, serde_config: SerdeConfig, compressed: bool = False) -> Any:
    if compressed:
        s = zlib.decompress(base64.decodebytes(s.encode('utf-8'))).decode('utf-8')
    return json.loads(s, object_hook=serde_config.deserialize)


def dumps(o: Any, serde_config: SerdeConfig, compressed: bool = False) -> str:
    o = serde_config.serialize(o)
    result = json.dumps(o)
    if compressed:
        result = base64.encodebytes(zlib.compress(result.encode('utf-8'))).decode('utf-8')
    return result

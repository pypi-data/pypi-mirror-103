from abc import ABC
from dataclasses import dataclass

from terality_serde import SerdeMixin


class TeralityError(SerdeMixin, Exception, ABC):
    """Base class for all Terality errors"""
    pass


@dataclass
class TeralityAuthError(TeralityError):
    message: str


@dataclass
class TeralityInternalError(TeralityError):
    message: str


@dataclass
class TeralityInvalidRequest(TeralityError):
    message: str


@dataclass
class TeralityNotSupportedError(TeralityError):
    message: str


# class PandasError(TeralityError):
#     pass
#
#
# class TeralityNotImplementedError(TeralityError):
#     pass
#
#
# class TeralityNotFoundError(TeralityError):
#     pass
#
#
# class TeralityExpiredError(TeralityError):
#     pass

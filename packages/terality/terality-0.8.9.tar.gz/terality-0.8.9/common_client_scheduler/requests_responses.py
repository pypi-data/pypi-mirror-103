from dataclasses import dataclass
from typing import Any, List, Optional, Type, Union

from terality_serde import SerdeMixin

from . import TransferConfig, TransferConfigLocal


""" Endpoints requests/responses """


@dataclass
class ErrorResponse(SerdeMixin):
    exception_class: Type
    args: List


@dataclass
class PendingComputationResponse(SerdeMixin):
    pending_computation_id: str


@dataclass
class ComputationResponse(SerdeMixin):
    result: Any
    inplace: bool


@dataclass
class CreateSessionResponse(SerdeMixin):
    id: str
    upload_config: Union[TransferConfig, TransferConfigLocal]
    download_config: Union[TransferConfig, TransferConfigLocal]


@dataclass
class DeleteSessionResponse(SerdeMixin):
    """Response to the delete session endpoint"""
    pass


@dataclass
class Upload(SerdeMixin):
    path: str


@dataclass
class UploadRequest(SerdeMixin):
    transfer_id: str
    aws_region: Optional[str]


@dataclass
class ExportRequest(SerdeMixin):
    path: str
    aws_region: Optional[str]


@dataclass
class ExportResponse(SerdeMixin):
    path: str
    aws_region: Optional[str]
    is_folder: bool
    transfer_id: str

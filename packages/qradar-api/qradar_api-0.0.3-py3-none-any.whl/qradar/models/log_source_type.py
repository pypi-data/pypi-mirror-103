from typing import List
from .qradarmodel import QRadarModel


class LogsourceType(QRadarModel):

    def __init__(self, *, id: int = None, name: str = None, internal: bool = None, custom: bool = None, protocol_types: List = None,
                 default_protocol_id: int = None, log_source_extension_id: int = None, supported_language_ids: List = None, version: str = None):
        self.id = id
        self.name = name
        self.internal = internal
        self.custom = custom
        self.protocol_types = protocol_types
        self.default_protocol_id = default_protocol_id
        self.log_source_extension_id = log_source_extension_id
        self.supported_language_ids = supported_language_ids
        self.version = version

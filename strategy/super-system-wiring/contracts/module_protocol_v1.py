from __future__ import annotations
from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, Field

PROTOCOL = "qdw-module"
PROTOCOL_VERSION = "1.0.0"

class Frozen(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

class Envelope(Frozen):
    protocol: Literal["qdw-module"] = PROTOCOL
    protocol_version: Literal["1.0.0"] = PROTOCOL_VERSION
    request_id: str
    module_id: str
    payload: dict[str, Any] = Field(default_factory=dict)

class ProgramStatus(Frozen):
    program_id: str
    state: str
    capability_demand: dict[str, float] = Field(default_factory=dict)
    possible_actions: list[str] = Field(default_factory=list)
    economics: dict[str, Any] = Field(default_factory=dict)

class ModuleStatusPayload(Frozen):
    module_id: str
    module_name: str
    programs: list[ProgramStatus] = Field(default_factory=list)

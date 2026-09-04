from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class Capability:
    discovery_api: bool = False
    researcher_submit_api: bool = False
    status_api: bool = False
    comments_api: bool = False
    agent_identity: bool = False
    transport: str = "portal"

class AdapterError(RuntimeError): pass
class ScopeChanged(AdapterError): pass
class HumanApprovalRequired(AdapterError): pass

class OpportunityAdapter(ABC):
    capability = Capability()

    @abstractmethod
    def list_opportunities(self, since: Optional[str] = None) -> list[dict]: ...

    @abstractmethod
    def get_opportunity(self, external_id: str) -> dict: ...

    @abstractmethod
    def snapshot_rules(self, external_id: str) -> dict:
        """Return canonical rules + timestamp + sha256."""

    @abstractmethod
    def build_submission(self, finding: dict) -> dict: ...

    def submit(self, finding: dict, approval_token: Optional[dict] = None) -> dict:
        if not self.capability.researcher_submit_api:
            raise HumanApprovalRequired(
                "No verified researcher-side submit API. Render a handoff bundle."
            )
        if not approval_token or approval_token.get("finding_id") != finding.get("finding_id"):
            raise HumanApprovalRequired("A finding-bound human approval token is required.")
        raise NotImplementedError

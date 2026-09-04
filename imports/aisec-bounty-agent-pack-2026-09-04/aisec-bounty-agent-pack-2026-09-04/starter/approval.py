from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(frozen=True)
class ApprovalToken:
    approval_id: str
    finding_id: str
    platform: str
    program_id: str
    scope_sha256: str
    action: str  # TEST or SUBMIT
    expires_at: str

    def valid_now(self) -> bool:
        expiry = datetime.fromisoformat(self.expires_at.replace("Z","+00:00"))
        return datetime.now(timezone.utc) < expiry

def assert_approval(token: ApprovalToken, *, action: str, scope_sha256: str):
    if token.action != action:
        raise PermissionError("Wrong approval action.")
    if token.scope_sha256 != scope_sha256:
        raise PermissionError("Scope changed since approval.")
    if not token.valid_now():
        raise PermissionError("Approval expired.")

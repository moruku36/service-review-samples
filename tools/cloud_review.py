"""Offline selected-control demonstration. Never connects to cloud APIs."""
import json
import sys
from pathlib import Path

FIELDS = {"provider", "admin_mfa_enforced", "storage_public", "unrestricted_admin_ingress"}
CONTROLS = (("admin_mfa_enforced", False, "IDENTITY_MFA"),
            ("storage_public", True, "STORAGE_PUBLIC"),
            ("unrestricted_admin_ingress", True, "ADMIN_INGRESS"))

def review(snapshot):
    if not isinstance(snapshot, dict) or set(snapshot) != FIELDS:
        raise ValueError("Expected exactly the documented normalized snapshot fields")
    if snapshot["provider"] not in ("AWS", "Azure", "Google Cloud"):
        raise ValueError("Unsupported provider")
    observations, gaps = [], []
    for field, concerning, control in CONTROLS:
        value = snapshot[field]
        if value is None:
            gaps.append(control)
        elif type(value) is not bool:
            raise ValueError("Control values must be boolean or null")
        elif value == concerning:
            observations.append(control)
    return {"provider": snapshot["provider"], "observations": observations,
            "evidence_gaps": gaps, "status": "SELECTED_FIELDS_ONLY_NOT_A_SAFETY_VERDICT"}

def main():
    try:
        if len(sys.argv) != 2:
            raise ValueError("Usage: python tools/cloud_review.py snapshot.json")
        source = Path(sys.argv[1])
        if source.stat().st_size > 4096:
            raise ValueError("Snapshot exceeds demonstration size limit")
        print(json.dumps(review(json.loads(source.read_text(encoding="utf-8"))), indent=2))
        return 0
    except (ValueError, OSError, UnicodeError):
        print("Invalid snapshot or unavailable file; no assessment produced", file=sys.stderr)
        return 2

if __name__ == "__main__":
    sys.exit(main())

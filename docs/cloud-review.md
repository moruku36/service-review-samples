# Cloud configuration review method

One provider, one environment, three explicitly named items at most. Review redacted configuration/IaC and contextual diagrams. Do not request root credentials, deploy changes or run production attack tests.

| Focus | AWS examples | Azure examples | Google Cloud examples |
|---|---|---|---|
| Identity and privilege | IAM policy/role, console MFA evidence | Entra role assignment and MFA enforcement evidence | IAM bindings and identity/MFA enforcement evidence |
| Storage visibility | S3 policy and public-access configuration | Storage container anonymous-access settings | Cloud Storage IAM and public-access prevention |
| Network exposure | One security group's inbound rules | One NSG's inbound rules | One VPC firewall ingress rule set |

These are review targets, not equivalent controls across providers. Record policy inheritance, exceptions, intended public access and the actual enforcement point. A public website can legitimately need public ingress; exposure is a review signal, not automatically a vulnerability.

## Offline demonstration

`tools/cloud_review.py` accepts a deliberately normalized JSON fixture with three boolean-or-null fields: `admin_mfa_enforced`, `storage_public`, `unrestricted_admin_ingress`. A reviewer manually maps supplied evidence to these fields. The tool does not infer real cloud state, provider-specific policy behavior, or complete effective permissions.

False MFA enforcement, public storage and unrestricted administrative ingress produce review observations. Null produces an evidence gap. No observations means only that the three supplied booleans did not trigger a concern; it is never a safe verdict. Invalid or extra fields are rejected to avoid unintentionally processing arbitrary secret data.

## Report

For each item: identify redacted evidence, expected use, observation, impact hypothesis, priority and a provider-appropriate next step. Mark missing effective-policy evidence and inherited configuration as limitations. Changes/retests require a new agreement.

# Fictional cloud configuration report

**Offline fixture demonstration, not a live cloud assessment.**

Artifacts: `fixtures/aws.json`, `fixtures/azure.json`, `fixtures/gcp.json`. These are normalized teaching inputs, not native provider exports. Scope is the three boolean fields documented in the method.

| Fixture | Observation | Suggested next step |
|---|---|---|
| AWS | MFA evidence says not enforced; storage public; unrestricted admin ingress | Verify identity enforcement, intentional data visibility, and narrow administrative access |
| Azure | MFA evidence unknown; storage not public; admin ingress not unrestricted | Request applicable identity-policy evidence; do not infer safety from other two flags |
| Google Cloud | MFA enforcement supplied; storage public; admin ingress unknown | Check intended storage audience and effective IAM; request ingress evidence |

The checker reports only named control IDs and evidence gaps. It does not establish exploitability, compliance or complete effective permissions. No real account identifiers, credentials or customer data are included. No cloud resource was created or changed.

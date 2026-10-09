# Login and access-control review method

1. Agree one feature, expected user roles, asset ownership and forbidden actions. Record code revision and artifact list.
2. Trace login/session handling and server-side authorization for that feature. Distinguish authentication from permission to access a particular record.
3. Read supplied routes, queries and policies for ownership/tenant restrictions. Review how privileged keys are referenced without collecting their values.
4. Compare anonymous, user A, user B and administrator expectations with code evidence. Do not run traffic against production. Any optional local test uses fictional accounts in an expressly authorized isolated environment.
5. Report specific observations with file/line or artifact references. Distinguish observed behavior, code-based inference and unknown runtime behavior.
6. Give prioritized corrective suggestions and remaining questions. Do not implement or claim a verified fix as part of the review.

This is a focused review, not a whole application audit. Database policies not supplied remain unverified even if the application code appears restricted.

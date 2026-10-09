# Focused app and cloud review samples

[日本語](README.ja.md)

Small, evidence-based review packages by Kentaro Mori: AI-built web app access controls, cloud configuration, and Japanese web app usability.

## What you can inspect

- [Service scope and prices](docs/services.md)
- [Login and access-control review method](docs/access-review.md) and [fictional report](samples/access-report.md)
- [AWS / Azure / Google Cloud review method](docs/cloud-review.md), [offline checker](tools/cloud_review.py), and [fictional findings](samples/cloud-report.md)
- [Japanese UI and workflow review method](docs/japanese-review.md) and [fictional report](samples/japanese-report.md)
- [Marketplace listing copy](docs/listings.md)
- [Verified marketplace publication status](docs/marketplace-status.md)
- [Validation record](docs/validation.md)

These samples use fictional data. They are not client work, a certification, a penetration test, or evidence that a live environment is secure. The offline checker demonstrates three selected checks on a manually normalized snapshot; it does not connect to a cloud account or parse native provider exports.

Existing technical work: [multi-cloud Terraform validation](https://github.com/moruku36/cloud-validation-level2-multicloud), [localhost web security lab](https://github.com/moruku36/web-security-control-lab). Consult each repository's status and limits; lab results do not establish customer outcomes.

Run the local demonstration with Python 3.10+:

```text
python -m unittest discover -s tests -v
python tools/cloud_review.py fixtures/aws.json
python tools/cloud_review.py fixtures/azure.json
python tools/cloud_review.py fixtures/gcp.json
```

No credentials, cloud subscription, external AI service, or extra Python dependencies are needed.

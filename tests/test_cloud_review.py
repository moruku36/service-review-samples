import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("cloud_review", ROOT / "tools/cloud_review.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class ReviewTests(unittest.TestCase):
    def fixture(self, name):
        return json.loads((ROOT / "fixtures" / (name + ".json")).read_text())

    def test_aws_three_observations(self):
        self.assertEqual(module.review(self.fixture("aws"))["observations"],
                         ["IDENTITY_MFA", "STORAGE_PUBLIC", "ADMIN_INGRESS"])

    def test_azure_unknown_is_evidence_gap(self):
        report = module.review(self.fixture("azure"))
        self.assertEqual(report["evidence_gaps"], ["IDENTITY_MFA"])
        self.assertEqual(report["observations"], [])
        self.assertIn("NOT_A_SAFETY_VERDICT", report["status"])

    def test_gcp_observation_and_gap(self):
        report = module.review(self.fixture("gcp"))
        self.assertEqual(report["observations"], ["STORAGE_PUBLIC"])
        self.assertEqual(report["evidence_gaps"], ["ADMIN_INGRESS"])

    def test_wrong_type_and_integer_rejected(self):
        for value in ("false", 0, [], {}):
            snapshot = self.fixture("aws")
            snapshot["storage_public"] = value
            with self.assertRaises(ValueError):
                module.review(snapshot)

    def test_extra_missing_and_unsupported_rejected(self):
        for change in ("extra", "missing", "provider"):
            snapshot = self.fixture("aws")
            if change == "extra": snapshot["secret"] = "SYNTHETIC_DO_NOT_PRINT"
            if change == "missing": del snapshot["storage_public"]
            if change == "provider": snapshot["provider"] = "Other"
            with self.assertRaises(ValueError): module.review(snapshot)

    def test_all_clear_still_no_safety_verdict(self):
        snapshot = self.fixture("azure")
        snapshot["admin_mfa_enforced"] = True
        report = module.review(snapshot)
        self.assertEqual(report["observations"], [])
        self.assertIn("NOT_A_SAFETY_VERDICT", report["status"])

    def test_cli_rejects_secret_without_echo(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.json"
            path.write_text('{"secret":"SYNTHETIC_DO_NOT_PRINT"}')
            result = subprocess.run([sys.executable, str(ROOT / "tools/cloud_review.py"), str(path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("SYNTHETIC_DO_NOT_PRINT", result.stdout + result.stderr)

    def test_cli_fixture_valid(self):
        result = subprocess.run([sys.executable, str(ROOT / "tools/cloud_review.py"), str(ROOT / "fixtures/aws.json")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["provider"], "AWS")

if __name__ == "__main__": unittest.main()

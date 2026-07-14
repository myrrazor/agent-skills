import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "summarize_calibration.py"


class SummarizeCalibrationTests(unittest.TestCase):
    def run_script(self, contents=None, *args):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "calibration.csv"
            if contents is not None:
                path.write_text(contents, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), *args, str(path)],
                capture_output=True,
                text=True,
                check=False,
            )
            return result

    def test_summarizes_records(self):
        csv = (
            "timestamp,task_id,predicted_likelihood,prediction_confidence,"
            "context_profile,claude_code_version,requested_model,served_model,"
            "fallback,category,notes\n"
            "2026-07-11,T1,low,high,low,2.1.170,fable,fable,false,none,ok\n"
            "2026-07-11,T2,medium,medium,medium,2.1.170,fable,opus,true,cyber,flagged\n"
        )
        result = self.run_script(csv)
        self.assertEqual(result.returncode, 0)
        self.assertIn("Overall: 1/2 fallbacks (50.0%).", result.stdout)
        self.assertIn("| medium | 1 | 1 | 100.0% |", result.stdout)

    def test_rejects_missing_columns(self):
        result = self.run_script("task_id,fallback\nT1,false\n")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Missing required columns:", result.stderr)

    def test_rejects_missing_file(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "/tmp/does-not-exist-calibration.csv"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("File not found:", result.stderr)


if __name__ == "__main__":
    unittest.main()

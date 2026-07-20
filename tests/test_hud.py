import os
import pathlib
import subprocess
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
HUD = ROOT / "bin/codex-hud"


def run(*args):
    env = {**os.environ, "NO_COLOR": "1"}
    return subprocess.run(
        [str(HUD), *args],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        timeout=15,
    )


class HudTests(unittest.TestCase):
    def test_full_frame(self):
        result = run()
        self.assertEqual(result.returncode, 0, result.stderr)
        for marker in (
            "CODEX HUD+",
            "MODEL",
            "TOKENS",
            "ACCOUNT",
            "agents:",
            "SYSTEM",
            "OMX",
        ):
            self.assertIn(marker, result.stdout)

    def test_compact_frame(self):
        result = run("--compact")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("\n", result.stdout.strip())
        self.assertIn("mdl:", result.stdout)
        self.assertIn("tok c:", result.stdout)

    def test_no_secret_value_output(self):
        source = (
            (ROOT / "bin/codex-hud").read_text()
            + (ROOT / "README.md").read_text()
            + (ROOT / "SECURITY.md").read_text()
        )
        self.assertNotRegex(source, r"/home/[A-Za-z0-9._-]+")
        self.assertNotRegex(
            source, r"(?:ghp_|github_pat_|sk_live_|BEGIN [A-Z ]*PRIVATE KEY)"
        )

    def test_version(self):
        result = run("--version")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertRegex(result.stdout, r"CODEX HUD\+ \d+\.\d+\.\d+")

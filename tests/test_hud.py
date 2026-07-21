import os
import pathlib
import subprocess
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
HUD = ROOT / "bin/codex-hud"
CODO = ROOT / "bin/codo"


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
            "CODEX HUD",
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
        self.assertRegex(result.stdout, r"Codex HUD \d+\.\d+\.\d+")

    def test_codo_forwards_codex_options_and_loads_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            codex_home = root / ".codex"
            codex_home.mkdir()
            (codex_home / "codo.config.toml").write_text(
                'model_reasoning_effort = "medium"\n'
            )
            fake_codex = root / "codex"
            fake_codex.write_text(
                '#!/usr/bin/env bash\nprintf \'<%s>\\n\' "$@"\n'
            )
            fake_codex.chmod(0o700)
            env = {
                **os.environ,
                "CODEX_HOME": str(codex_home),
                "CODO_CODEX_COMMAND": str(fake_codex),
                "CODO_HUD": "off",
                "CODO_TMUX": "off",
            }
            result = subprocess.run(
                [str(CODO), "--search", "exec", "run tests"],
                cwd=ROOT,
                env=env,
                text=True,
                capture_output=True,
                timeout=15,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                result.stdout.splitlines(),
                ["<--profile>", "<codo>", "<--search>", "<exec>", "<run tests>"],
            )

            explicit = subprocess.run(
                [str(CODO), "--profile", "other", "--model", "chosen"],
                cwd=ROOT,
                env={**env, "CODO_MODEL": "environment-default"},
                text=True,
                capture_output=True,
                timeout=15,
            )
            self.assertEqual(explicit.returncode, 0, explicit.stderr)
            self.assertEqual(
                explicit.stdout.splitlines(),
                ["<--profile>", "<other>", "<--model>", "<chosen>"],
            )

    def test_active_session_options_override_base_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            sessions = root / "sessions/2026/07/20"
            sessions.mkdir(parents=True)
            (root / "config.toml").write_text(
                'model = "base-model"\nmodel_reasoning_effort = "low"\n'
            )
            (sessions / "rollout-test.jsonl").write_text(
                '{"type":"turn_context","payload":{"model":"active-model",'
                '"effort":"high","approval_policy":"never",'
                '"sandbox_policy":{"type":"danger-full-access"}}}\n'
                '{"type":"event_msg","payload":{"type":"token_count",'
                '"info":{"model_context_window":1000}}}\n'
            )
            result = subprocess.run(
                [str(HUD), "--compact"],
                cwd=ROOT,
                env={**os.environ, "NO_COLOR": "1", "CODEX_HOME": str(root)},
                text=True,
                capture_output=True,
                timeout=15,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("mdl:active-model/high", result.stdout)
            self.assertIn("pol:never/danger-full-access", result.stdout)

    def test_codo_removes_managed_hud_pane_on_exit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            log = root / "tmux.log"
            fake_codex = root / "codex"
            fake_hud = root / "codex-hud"
            fake_tmux = root / "tmux"
            fake_codex.write_text("#!/usr/bin/env bash\nexit 7\n")
            fake_hud.write_text("#!/usr/bin/env bash\nprintf 'HUD active in pane %%9\\n'\n")
            fake_tmux.write_text(
                f"#!/usr/bin/env bash\nprintf '%s\\n' \"$*\" >> {log!s}\n"
            )
            for command in (fake_codex, fake_hud, fake_tmux):
                command.chmod(0o700)
            result = subprocess.run(
                [str(CODO)],
                cwd=ROOT,
                env={
                    **os.environ,
                    "PATH": f"{root}:{os.environ['PATH']}",
                    "TMUX": "test",
                    "CODO_CODEX_COMMAND": str(fake_codex),
                    "CODO_HUD_COMMAND": str(fake_hud),
                },
                text=True,
                capture_output=True,
                timeout=15,
            )
            self.assertEqual(result.returncode, 7)
            self.assertEqual(log.read_text().strip(), "kill-pane -t %9")

    def test_installer_uses_non_repeating_status_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = pathlib.Path(tmp)
            fake_bin = home / "fake-bin"
            fake_bin.mkdir()
            for name in ("codex", "tmux"):
                command = fake_bin / name
                command.write_text("#!/usr/bin/env bash\nexit 0\n")
                command.chmod(0o700)
            (home / ".codex").mkdir()
            (home / ".codex/config.toml").write_text("")
            (home / ".tmux.conf").write_text(
                "before\n# CODEX-HUD+:START\nlegacy\n# CODEX-HUD+:END\nafter\n"
            )
            env = {
                **os.environ,
                "HOME": str(home),
                "PATH": f"{fake_bin}:{os.environ['PATH']}",
            }
            result = subprocess.run(
                [str(ROOT / "install.sh")],
                cwd=ROOT,
                env=env,
                text=True,
                capture_output=True,
                timeout=15,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            config = (home / ".codex/config.toml").read_text()
            self.assertIn('"model-with-reasoning"', config)
            self.assertIn('"context-remaining"', config)
            for duplicate in ('"project-root"', '"model-name"', '"context-used"'):
                self.assertNotIn(duplicate, config)
            self.assertTrue((home / ".local/bin/codo").is_file())
            tmux_config = (home / ".tmux.conf").read_text()
            self.assertNotIn("CODEX-HUD+", tmux_config)
            self.assertEqual(tmux_config.count("# CODEX-HUD:START"), 1)
            self.assertEqual(tmux_config.count("# CODEX-HUD:END"), 1)

    def test_installer_stops_and_announces_missing_prerequisite(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = {
                **os.environ,
                "HOME": tmp,
                "CODO_CODEX_COMMAND": "codex-definitely-not-installed",
            }
            result = subprocess.run(
                [str(ROOT / "install.sh"), "--check"],
                cwd=ROOT,
                env=env,
                text=True,
                capture_output=True,
                timeout=15,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("missing: Codex CLI", result.stderr)
            self.assertIn("no changes were made", result.stderr)
            self.assertFalse((pathlib.Path(tmp) / ".local/bin/codo").exists())

    def test_installer_does_not_require_unrelated_plugins(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            fake_bin = root / "fake-bin"
            fake_bin.mkdir()
            for name in ("codex", "tmux"):
                command = fake_bin / name
                command.write_text("#!/usr/bin/env bash\nexit 0\n")
                command.chmod(0o700)
            env = {
                **os.environ,
                "HOME": tmp,
                "PATH": f"{fake_bin}:{os.environ['PATH']}",
            }
            result = subprocess.run(
                [str(ROOT / "install.sh"), "--check"],
                cwd=ROOT,
                env=env,
                text=True,
                capture_output=True,
                timeout=15,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotIn("plugin", result.stdout.lower())
            self.assertNotIn("plugin", result.stderr.lower())
            self.assertFalse((root / ".local/bin/codo").exists())

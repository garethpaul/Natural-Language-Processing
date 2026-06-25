import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "test-default-sample-mutations.py"
SPEC = importlib.util.spec_from_file_location("default_sample_mutations", SCRIPT_PATH)
default_sample_mutations = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(default_sample_mutations)


class DefaultSampleMutationCopyTests(unittest.TestCase):
    def test_copy_tracked_checkout_excludes_ignored_local_environment(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source"
            destination = Path(directory) / "destination"
            source.mkdir()
            subprocess.run(["git", "init", "-q"], cwd=source, check=True)
            (source / ".gitignore").write_text(".venv/\n", encoding="utf-8")
            (source / "tracked.txt").write_text("tracked\n", encoding="utf-8")
            ignored = source / ".venv" / "bin"
            ignored.mkdir(parents=True)
            (ignored / "python").write_text("ignored\n", encoding="utf-8")
            subprocess.run(
                ["git", "add", ".gitignore", "tracked.txt"],
                cwd=source,
                check=True,
            )

            default_sample_mutations.copy_tracked_checkout(source, destination)

            self.assertEqual("tracked\n", (destination / "tracked.txt").read_text())
            self.assertTrue((destination / ".gitignore").is_file())
            self.assertFalse((destination / ".venv").exists())
            self.assertFalse((destination / ".git").exists())

    def test_copy_exported_checkout_honors_gitignore_without_git_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source"
            destination = Path(directory) / "destination"
            source.mkdir()
            (source / ".gitignore").write_text(".venv/\n*.log\n", encoding="utf-8")
            (source / "tracked.txt").write_text("tracked\n", encoding="utf-8")
            ignored = source / ".venv" / "bin"
            ignored.mkdir(parents=True)
            (ignored / "python").write_text("ignored\n", encoding="utf-8")
            (source / "debug.log").write_text("ignored\n", encoding="utf-8")

            default_sample_mutations.copy_tracked_checkout(source, destination)

            self.assertEqual("tracked\n", (destination / "tracked.txt").read_text())
            self.assertTrue((destination / ".gitignore").is_file())
            self.assertFalse((destination / ".venv").exists())
            self.assertFalse((destination / "debug.log").exists())


if __name__ == "__main__":
    unittest.main()

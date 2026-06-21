import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class MakefileRootTests(unittest.TestCase):
    def test_absolute_makefile_path_with_spaces_and_apostrophe(self):
        with tempfile.TemporaryDirectory(prefix="NLP's safe gate ") as directory:
            checkout = Path(directory)
            makefile = checkout / "Makefile"
            makefile.write_text(
                (ROOT / "Makefile").read_text(encoding="utf-8"), encoding="utf-8"
            )

            for target in ("clean", "compile", "test", "static-check"):
                with self.subTest(target=target):
                    result = subprocess.run(
                        ["make", "-n", "-f", str(makefile), target],
                        cwd=checkout.parent,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        check=False,
                        env={"PATH": os.environ.get("PATH", "")},
                    )

                    self.assertEqual(result.returncode, 0, result.stdout)
                    self.assertNotIn('find " ', result.stdout)
                    self.assertNotIn('cd " ', result.stdout)
                    self.assertNotIn('python3 " ', result.stdout)
                    self.assertIn(str(checkout), result.stdout)

    def test_makefile_list_override_fails_before_cleanup(self):
        result = subprocess.run(
            [
                "make",
                "-n",
                "-f",
                str(ROOT / "Makefile"),
                "MAKEFILE_LIST=/tmp/untrusted",
                "clean",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
            env={"PATH": os.environ.get("PATH", "")},
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("MAKEFILE_LIST must not be overridden", result.stdout)
        self.assertNotIn("find ", result.stdout)


if __name__ == "__main__":
    unittest.main()

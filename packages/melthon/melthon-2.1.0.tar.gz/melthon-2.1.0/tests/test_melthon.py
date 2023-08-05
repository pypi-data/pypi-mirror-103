import os
import unittest
from filecmp import dircmp
from pathlib import Path

from click.testing import CliRunner

from melthon.cli import main


class TestMelthon(unittest.TestCase):
    def test_help(self):
        runner = CliRunner()
        result = runner.invoke(main, [])

        # Melthon should show help page
        self.assertIsNone(result.exception)
        self.assertIn("Usage", result.output)
        self.assertEqual(result.exit_code, 0)


class TestIntegration(unittest.TestCase):
    def test_integration(self):
        os.chdir(Path(__file__).parent / "integration" / "src")
        runner = CliRunner()
        result = runner.invoke(main, "build")

        # Melthon should generate site
        self.assertIsNone(result.exception)
        self.assertNotIn("ERROR", result.output)
        self.assertEqual(result.exit_code, 0)

        # Compare result with expected
        dcmp = dircmp('output', '../expected')
        self._assert_dir_equal(dcmp)

        # Call clean command
        runner = CliRunner()
        result = runner.invoke(main, "clean")
        self.assertIsNone(result.exception)
        self.assertNotIn("ERROR", result.output)
        self.assertEqual(result.exit_code, 0)

        # Output dir should exist but be empty
        output_dir = Path('output')
        self.assertTrue(output_dir.is_dir(), "Output dir is missing")
        self.assertEqual(list(output_dir.iterdir()), [], "Output dir should be empty")
        output_dir.rmdir()

    def _assert_dir_equal(self, dcmp):
        for name in dcmp.diff_files:
            self.fail(f"File {name} is not equal in {dcmp.left} and {dcmp.right}")
        for name in dcmp.left_only:
            self.fail(f"File {name} is missing in {dcmp.left}")
        for name in dcmp.right_only:
            self.fail(f"Unexpected file {name} found in {dcmp.left}")
        for sub_dcmp in dcmp.subdirs.values():
            self._assert_dir_equal(sub_dcmp)


if __name__ == '__main__':
    unittest.main()

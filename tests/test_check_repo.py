import contextlib
import io
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from tools import check_repo as c


class FenceTests(unittest.TestCase):
    def test_long_fence_survives_short_inner_fence(self):
        masked = c.markdown_without_fenced_code("````md\n```\n[x](missing.md)\n````\n[y](real.md)")
        self.assertNotIn("missing", masked)
        self.assertIn("real", masked)

    def test_close_requires_same_character_and_only_trailing_space(self):
        for false_close in ("~~~", "```text", "``", "    ```"):
            with self.subTest(false_close=false_close):
                self.assertNotIn("hidden", c.markdown_without_fenced_code("```\n" + false_close + "\nhidden\n```"))

    def test_longer_close_is_valid(self):
        self.assertIn("shown", c.markdown_without_fenced_code("~~~python\nhidden\n~~~~ \nshown"))

    def test_unclosed_fence_masks_to_end(self):
        self.assertNotIn("hidden", c.markdown_without_fenced_code("```\nhidden"))

    def test_backtick_in_info_disables_backtick_opener(self):
        self.assertIn("shown", c.markdown_without_fenced_code("``` x`y\nshown"))

    def test_line_positions_preserved(self):
        original = "before\n```py\nhidden\n```\nafter"
        masked = c.markdown_without_fenced_code(original)
        self.assertEqual(len(original.splitlines()), len(masked.splitlines()))
        self.assertEqual(masked.splitlines()[-1], "after")


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        self.root_patch = patch.object(c, "ROOT", self.root)
        self.root_patch.start()
        self.git("init", "-q")
        self.write(".gitignore", "experiments/artifacts/**\n!experiments/artifacts/.gitkeep\nignored/**\n")
        self.write("experiments/artifacts/.gitkeep", "")
        self.write("README.md", "# Hello\n[link](doc.md#title)\n")
        self.write("doc.md", "# Title\n")
        self.git("add", ".")
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "fixture")

    def tearDown(self):
        self.root_patch.stop()
        self.temp.cleanup()

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, check=True, capture_output=True, text=True)

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def test_normal_links_and_public_untracked_files(self):
        self.write("new.md", "[hi](README.md#hello)")
        failures, count, links = c.check_markdown_links()
        self.assertEqual((failures, count, links), ([], 3, 2))

    def test_ignored_records_are_never_opened(self):
        hidden = self.write("experiments/artifacts/run/pilot.md", "[PRIVATE-CANARY](missing.md)")
        other = self.write("ignored/record.md", "[ANOTHER-CANARY](missing.md)")
        original = Path.read_text
        def guarded(path, *args, **kwargs):
            self.assertNotIn(path, {hidden, other})
            return original(path, *args, **kwargs)
        with patch.object(Path, "read_text", guarded):
            self.assertEqual(c.check_markdown_links(), ([], 2, 1))

    def test_forced_tracked_restricted_record_fails_without_content_read(self):
        hidden = self.write("experiments/artifacts/run/pilot.md", "PRIVATE-CANARY")
        self.git("add", "-f", str(hidden.relative_to(self.root)))
        with patch.object(Path, "read_text", side_effect=AssertionError("must not read")):
            with self.assertRaisesRegex(ValueError, "restricted artifact"):
                c.public_repository_files()

    def test_link_to_ignored_target_does_not_open_anchor(self):
        hidden = self.write("ignored/private.md", "# PRIVATE-CANARY")
        self.write("README.md", "[local](ignored/private.md#anything)")
        original = Path.read_text
        def guarded(path, *args, **kwargs):
            self.assertNotEqual(path, hidden)
            return original(path, *args, **kwargs)
        with patch.object(Path, "read_text", guarded):
            failures, _, _ = c.check_markdown_links()
        self.assertEqual(len(failures), 1)
        self.assertNotIn("PRIVATE-CANARY", "".join(failures))

    def test_tracked_newly_ignored_public_file_still_checked(self):
        self.write(".gitignore", "doc.md\n")
        self.write("doc.md", "[missing](gone.md)")
        self.assertTrue(c.check_markdown_links()[0])

    def test_symlink_source_fails_closed(self):
        hidden = self.write("ignored/private.md", "PRIVATE-CANARY")
        (self.root / "alias.md").symlink_to(hidden)
        with self.assertRaisesRegex(ValueError, "symlink"):
            c.public_repository_files()

    def test_symlink_parent_fails_closed(self):
        self.write("nested/doc.md", "safe")
        self.git("add", "nested/doc.md")
        (self.root / "nested/doc.md").unlink()
        (self.root / "nested").rmdir()
        target = self.root / "ignored"
        target.mkdir(exist_ok=True)
        (self.root / "nested").symlink_to(target, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            c.public_repository_files()

    def test_git_failure_has_no_recursive_fallback(self):
        with patch.object(subprocess, "run", side_effect=subprocess.CalledProcessError(1, "git")), \
             patch.object(Path, "rglob", side_effect=AssertionError("must not walk")):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(c.main(), 1)
        self.assertIn("no recursive scan", output.getvalue())

    def test_unicode_space_and_newline_filenames_are_not_git_quoted(self):
        names = ("中文 file.md", "line\nbreak.md")
        for name in names:
            self.write(name, "# OK")
        public = {p.relative_to(self.root).as_posix() for p in c.public_repository_files()}
        self.assertTrue(set(names).issubset(public))
        self.assertTrue(set(names).issubset(c.git_paths_changed_from_head()))

    def test_parent_git_repository_is_not_treated_as_checker_root(self):
        nested = self.root / "nested"
        nested.mkdir()
        with patch.object(c, "ROOT", nested):
            with self.assertRaisesRegex(ValueError, "not the Git worktree root"):
                c.public_repository_files()

    def test_path_escape_is_rejected(self):
        self.write("README.md", "[bad](../../outside.md)")
        self.assertIn("escapes the repository", c.check_markdown_links()[0][0])

    def test_deleted_file_is_missing_link(self):
        (self.root / "doc.md").unlink()
        self.assertTrue(c.check_markdown_links()[0])

    def test_directory_link_with_public_descendant(self):
        self.write("README.md", "[docs](docs/)")
        self.write("docs/a.md", "# A")
        self.assertFalse(c.check_markdown_links()[0])


if __name__ == "__main__":
    unittest.main()

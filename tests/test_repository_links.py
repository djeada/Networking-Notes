"""Check the inline relative links and study indexes used by this repository."""

from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\]\(([^\s)]+)(?:\s+[^)]*)?\)")


def local_links(path):
    # Examples inside fenced code are not navigational links.
    content = re.sub(r"^(`{3,}|~{3,}).*?^\1[^\n]*$", "", path.read_text(encoding="utf-8"),
                     flags=re.MULTILINE | re.DOTALL)
    for target in LINK.findall(content):
        url = urlsplit(target.strip("<>"))
        if not url.scheme and not url.netloc and url.path:
            yield (path.parent / unquote(url.path)).resolve()


class RepositoryLinkTests(unittest.TestCase):
    def test_relative_file_links_exist(self):
        files = [ROOT / "README.md"]
        for folder in ("notes", "practice", "quizzes", "scripts"):
            files.extend((ROOT / folder).rglob("*.md"))
        for path in files:
            for target in local_links(path):
                with self.subTest(source=str(path.relative_to(ROOT)), target=str(target)):
                    self.assertTrue(target.is_relative_to(ROOT), "Link escapes the repository")
                    self.assertTrue(target.exists(), "Linked file or directory does not exist")

    def test_all_notes_and_quizzes_appear_in_main_index(self):
        links = set(local_links(ROOT / "README.md"))
        for folder in ("notes", "quizzes"):
            for path in (ROOT / folder).rglob("*.md"):
                with self.subTest(path=str(path.relative_to(ROOT))):
                    self.assertIn(path, links)

    def test_all_educational_scripts_appear_in_script_index(self):
        links = set(local_links(ROOT / "scripts" / "README.md"))
        for path in (ROOT / "scripts").rglob("*.py"):
            with self.subTest(path=str(path.relative_to(ROOT))):
                self.assertIn(path, links)


if __name__ == "__main__":
    unittest.main()

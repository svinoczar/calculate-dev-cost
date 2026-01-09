import os
import fnmatch
from data.domain.commit import Commit
from util.logger import logger


class FilesFilter:
    def __init__(self, ignore_file: str = ".dcoignore"):
        self.ignore_patterns = self._load_ignore_patterns(ignore_file)

    def _load_ignore_patterns(self, path: str) -> list[str]:
        if not os.path.exists(path):
            logger.warning(f"{path} not found, no files ignored")
            return []

        with open(path, "r", encoding="utf-8") as f:
            patterns = [
                line.strip()
                for line in f
                if line.strip() and not line.startswith("#")
            ]

        logger.info(f"Loaded ignore patterns: {patterns}")
        return patterns

    def filter(self, commit: Commit) -> Commit:
        # print(self.ignore_patterns)
        
        before = len(commit.files)

        commit.files = [
            f for f in commit.files
            if self._is_allowed(f.filename)
        ]

        after = len(commit.files)

        if before != after:
            logger.debug(
                f"Commit {commit.sha}: filtered {before - after} files"
            )

        return commit

    def _is_allowed(self, filename: str) -> bool:
        # скрытые файлы
        if filename.startswith("."):
            return False
        # match по .dcoignore (glob, а не endswith)
        for pattern in self.ignore_patterns:
            if filename.endswith(pattern):
                print('pipipiski')
                return False

        return True
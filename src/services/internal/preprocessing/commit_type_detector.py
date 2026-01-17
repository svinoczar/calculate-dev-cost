from collections import defaultdict
import fnmatch
import re
from data.domain.commit import Commit
from data.enums.analytics import COMMIT_TYPE_PATTERNS, CONVENTIONAL_COMMIT_PATTERN


class CommitTypeDetector:
    def detect(self, commit: Commit) -> tuple[str, float]:
        msg = commit.message.lower()

        # 1. Conventional commits
        if re.match(CONVENTIONAL_COMMIT_PATTERN, msg):
            ctype = msg.split(":")[0].split("(")[0]
            return ctype, 0.9

        # 2. File-based heuristics
        scores = defaultdict(int)

        for file in commit.files:
            for ctype, meta in COMMIT_TYPE_PATTERNS.items():
                for pattern in meta["file_patterns"]:
                    if fnmatch.fnmatch(file.path, pattern):
                        scores[ctype] += 1

        if scores:
            best = max(scores, key=scores.get)
            confidence = min(0.4 + scores[best] * 0.1, 0.8)
            return best, confidence

        return "unknown", 0.2

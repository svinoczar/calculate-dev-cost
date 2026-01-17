from typing import Optional

from src.data.domain.commit import Commit
from src.services.internal.preprocessing.file_language_enricher import FileLanguageEnricher
from src.services.internal.preprocessing.commit_type_detector import CommitTypeDetector


class CommitEnricher:
    def __init__(
        self,
        file_enricher: FileLanguageEnricher,
        commit_type_detector: CommitTypeDetector,
    ):
        self.file_enricher = file_enricher
        self.commit_type_detector = commit_type_detector

    def enrich(self, commit: Commit) -> Commit:
        if not commit.files:
            commit.commit_type = "unknown"
            commit.commit_type_confidence = 0.0
            return commit

        for file in commit.files:
            self.file_enricher.enrich(file)

        commit_type, confidence = self.commit_type_detector.detect(commit)

        commit.commit_type = commit_type
        commit.commit_type_confidence = confidence

        return commit

from src.data.domain.file_change import FileChange


class FileLanguageEnricher:
    def __init__(self, detector):
        self.detector = detector

    def enrich(self, file: FileChange) -> FileChange:
        lang = self.detector.detect(file.filename)
        file.language = lang

        return file

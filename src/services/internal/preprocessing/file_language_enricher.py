from src.data.domain.file_change import FileChange


class FileLanguageEnricher:
    def __init__(self, detector):
        self.detector = detector

    def enrich(self, file: FileChange) -> FileChange:
        lang, conf = self.detector.detect(file.filename, file.patch)
        file.language = lang
        file.language_confidence = conf

        return file

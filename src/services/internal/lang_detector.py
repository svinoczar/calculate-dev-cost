from data.enums.language import FILE_EXTENSIONS, FUNCTION_PATTERNS, CLASS_PATTERNS, IMPORT_PATTERNS

from transformers import AutoTokenizer
from onnxruntime import InferenceSession
import numpy as np
import os
import json
import re


"""
    Было решено отказаться от ML модели для распознавания языка из-за низкой точности,
    особенно на коротких фрагментах кода или инлайнах фрагментах, а также
    из-за сложности поддержки такой модели, то есть  в следствии неэфектиности ее использовния.
"""
# class LanguageDetectorModel:
#     def __init__(self):
#         # FIXME: remove return, check __init__ for no internet work
#         # return
#         base_dir = os.path.dirname(__file__)
#         model_dir = os.path.join(
#             base_dir, "..", "..", "models", "lang_detect"
#         )

#         self.session = InferenceSession(
#             os.path.join(model_dir, "model.onnx"),
#             providers=["CPUExecutionProvider"]
#         )

#         self.tokenizer = AutoTokenizer.from_pretrained(
#             "philomath-1209/programming-language-identification"
#         )

#         with open(os.path.join(model_dir, "config.json"), "r", encoding="utf-8") as f:
#             cfg = json.load(f)
#             self.id2label = {int(k): v for k, v in cfg["id2label"].items()}

#     def detect(self, code: str, threshold: float = 0.7):
#         inputs = self.tokenizer(
#             code,
#             return_tensors="np",
#             truncation=True,
#             max_length=512
#         )

#         ort_inputs = {
#             "input_ids": inputs["input_ids"],
#             "attention_mask": inputs["attention_mask"]
#         }

#         logits = self.session.run(None, ort_inputs)[0][0]
#         probs = self._softmax(logits)

#         idx = int(np.argmax(probs))
#         confidence = float(probs[idx])

#         if confidence < threshold:
#             return "Unknown", confidence

#         return self.id2label[idx], confidence

#     @staticmethod
#     def _softmax(x):
#         e = np.exp(x - np.max(x))
#         return e / e.sum()


class LanguageDetector:
    def __init__ (self):
        pass
    
    def detect(self, filename: str, patch: str | None):
        lang = self._by_extension(filename)
        if not lang:
            return "Unknown", 0.0
        
        confidence = 1

        if patch:
            score = self._score_by_patterns(lang, patch)
            confidence += min(score * 0.1, 0.3)

        return lang, min(confidence, 0.9)
    
    def _by_extension(self, filename: str):
        ext = os.path.splitext(filename)[1].lstrip('.').lower()
        return FILE_EXTENSIONS.get(ext)
    
    def _score_by_patterns(self, lang: str, text: str) -> int:
        score = 0

        for pattern in FUNCTION_PATTERNS.get(lang, []):
            if re.search(pattern, text, re.MULTILINE):
                score += 2

        for pattern in CLASS_PATTERNS.get(lang, []):
            if re.search(pattern, text, re.MULTILINE):
                score += 2

        for pattern in IMPORT_PATTERNS.get(lang, []):
            if re.search(pattern, text, re.MULTILINE):
                score += 1

        return score
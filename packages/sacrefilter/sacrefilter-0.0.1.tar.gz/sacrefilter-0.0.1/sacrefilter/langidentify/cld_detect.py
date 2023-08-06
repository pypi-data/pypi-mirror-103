
import pycld2


class CLD2:
    def __init__(self):
        # Fetch the model's supported language labels.
        _, self._classes = zip(*pycld2.LANGUAGES)

    def classify(self, text: str, n_best: int=1):
        try:
            # `pycld2.detect` with returnVecrtors returns a tuple of
            # -> (is_reliable, text_bytes_found, details, chunk_offsets)
            _, _, details, _ = pycld2.detect(text, returnVectors=True)
            # `details` is a list of tuple that contains
            # -> [(CLD2::LanguageName, CLD2::LanguageCode, percent, normalized_score), ...]
            # Note: Normalized score is out of 1000, so we need to divide by 100.
            if n_best == 1:
                return details[0][1], details[0][3] / 100
            else:
                return [(l[1], l[3]/100) for l in details]
        except Exception:
            return ('un', 0.0) if n_best == 1 else [('un', 0.0)]

    def confidence(self, text, lang):
        predicted_lang, predicted_confidence = self.classify(text)
        # Return 0 if predicted lang is not expected, else return confidence.
        return 0.0 if lang != predicted_lang else predicted_confidence

    def supported_languages(self):
        return self._classes

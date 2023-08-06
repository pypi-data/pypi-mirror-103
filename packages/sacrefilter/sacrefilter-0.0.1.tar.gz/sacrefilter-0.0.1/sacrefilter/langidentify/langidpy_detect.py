
import numpy as np

from langid.langid import LanguageIdentifier
from langid.langid import model as langid_model


"""
References:
 - https://stackoverflow.com/questions/39142778/python-how-to-determine-the-language
 - https://github.com/ovalhub/pyicu/issues/70
 - https://stackoverflow.com/questions/29777337/macosx-boost-python-pyftgl-symbol-not-found-expected-in-flat-namespace
"""

class LangIdPy:
    def __init__(self, lang_set: List[str]=None):
        # Initializing langid.py this way so that we get normalized probs.
        self._model = LanguageIdentifier.from_modelstring(langid_model, norm_probs=True)
        if language_set:
            self._model.set_languages(lang_set)
        # Fetch the model's supported language labels.
        self._classes = [str(c) for c in self.nb_classes]

    def classify(self, text:str, n_best: int=1):
        feature_value = self._model.instance2fv(text)
        probs = self._model.norm_probs(self._model.nb_classprobs(feature_value))

        if n_best == 1:
            best_class = np.argmax(probs)  # Gets best class index.
            return str(self._classes[best_class], float(probs[best_class])
        else:
            n_best_classes = (-probs).argsort()[:n_best]  # Gets Nbest class indices.
            return [(self._classes[c], float(probs[c])) for c in n_best_classes]

    def confidence(self, text:str, lang:str):
        # Get the one best, prediction.
        try:
            predicted_lang, predicted_confidence = self.classify(text)
        except:
            predicted_lang, predicted_confidence = ('un', 0.0)
        # Return 0 if predicted lang is not expected, else return confidence.
        return 0.0 if lang != predicted_lang else predicted_confidence

    def supported_languages(self):
        return self._classes

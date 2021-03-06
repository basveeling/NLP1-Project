from feature_extractor import FeatureExtractor
from feature_lib.helper_functions import *
import numpy as np

class NGramFreq(FeatureExtractor):
    def __init__(self,n,num_words,common_vocabulary=None):
        self.n = n
        self.num_words = num_words
        self.common_vocabulary = common_vocabulary
        FeatureExtractor.__init__(self)

    def quantize_feature(self, texts, labels):
        if self.common_vocabulary is None:
            self.common_vocabulary = n_gram_vocabulary(texts,self.n,self.num_words)

        n_gram_freq_matrix = np.zeros((len(texts),self.num_words))
        for index,text in enumerate(texts):
            # TODO: this doesn't take n-grams into account, now we compare ngrams with individual words
            count_dict = non_stop_word_count(text)
            # TODO: Normalize by number of words in documents
            n_gram_freqs = np.double(np.array([count_dict.get(key_word,0) for key_word in self.common_vocabulary]))
            # Normalize it
            n_gram_freqs = self._normalize_freq(n_gram_freqs,text)
            n_gram_freq_matrix[index,:] = n_gram_freqs

        return n_gram_freq_matrix

    def _normalize_freq(self, n_gram_freqs,text):
        with np.errstate(divide='ignore'):
            res = np.divide(n_gram_freqs, float(num_n_grams_in_document(text)))
        res[np.isnan(res)] = 0
        return res
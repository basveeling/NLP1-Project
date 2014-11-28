import numpy.random as rnd
import numpy as np

class Data(object):
    def __init__(self):
        pass

    def all(self):
        return self._data(), self._labels()

    def fold(self, training_ratio=0.5, testing_ratio=0.25):
        assert training_ratio + testing_ratio <= 1

        n = self._number_of_samples()
        last_training_index = int(np.floor(n * training_ratio))
        last_testing_index = int(np.floor(n * (training_ratio + testing_ratio)))
        index_permutation = rnd.permutation(n)

        training_indexes = index_permutation[0:last_training_index]
        testing_indexes = index_permutation[last_training_index + 1:last_testing_index]

        return self._data()[training_indexes], self._labels()[training_indexes], self._data()[testing_indexes], self._labels()[testing_indexes]

    def bootstrap(self):
        n = self._number_of_samples()
        last_index = int(np.floor(n * 0.6))
        indexes = rnd.permutation(n)[0:last_index]
        return self._data()[indexes], self._labels()[indexes]

    # To be subclassed
    def _labels(self):
        assert False, "Should be subclassed"

    def _data(self):
        assert False, "Should be subclassed"

    def _number_of_samples(self):
        assert False, "Should be subclassed"
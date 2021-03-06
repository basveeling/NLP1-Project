import numpy as np
# import MySQLdb as mdb
from classification_models.randomForestCM import *
# from classification_models.averaged_perceptronCM import *
from datasets.mysql_dataset import MysqlDataset
from data.dataset_data import MysqlDatasetData
from feature_extractors.factor_stop_words import FactorStopWordsFE
from feature_extractors.ngram_freq import NGramFreq
# from feature_extractors.words_per_sentence import WordsPerSentanceFE
from feature_extractors.word_freq import WordFreqFE
from feature_extractors.pos_tag_hist import PosTagHistFE

# Import data
features = [
    # FactorStopWordsFE(),
    PosTagHistFE(),
    # WordsPerSentanceFE(), # Not implemented properly yet!
    NGramFreq(2, 400),
    WordFreqFE(400)
]
dataset = MysqlDatasetData(MysqlDataset("small_article"), features)

data_train, labels_train, data_test, labels_test = dataset.fold(n_test=1)
# Train model
model = RandomForestCM(n_estimators=20000)
model.train_classifier(data_train, labels_train)

# Test model
q, pred_labels = model.test_classifier(data_test, labels_test)
print q
print pred_labels

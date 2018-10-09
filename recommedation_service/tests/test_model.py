import pytest
import scipy
import implicit

from recommendation_app import Recommender


class Parser:
    def call(self, user_id):
        return {'artist': ['Lykke Li', 'Kings Of Convenience', 'Beach House']}


def test_init():
    recommender = Recommender(n_recommendations=55, novelty_level=15)
    assert recommender.model is not None
    assert len(recommender.artist_names) > 0
    assert recommender.dataset_s.shape[0] > 0
    assert recommender.dataset_s.shape[1] > 0
    assert type(recommender.dataset_s) is scipy.sparse.csr.csr_matrix
    assert recommender.parser is None
    assert recommender.novelty_level == 15
    assert recommender.n_recommendations == 55


def test_predict():
    recommender = Recommender(n_recommendations=6)
    recommender.parser = Parser()
    bands_6 = recommender.predict(1)
    assert len(bands_6) == 6

    recommender = Recommender(n_recommendations=80)
    recommender.parser = Parser()
    bands = recommender.predict(11)
    assert len(bands) == 80
    assert type(bands) is list

    assert bands_6 == bands[:6]
    assert type(bands[0]) is str

    assert set(['Lykke Li', 'Kings Of Convenience', 'Beach House']).intersection(bands) == set()

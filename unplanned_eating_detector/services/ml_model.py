import numpy as np
from sklearn.linear_model import LogisticRegression


class MLModel:

    def __init__(self):
        self.model = LogisticRegression()
        self._train_model()

    def _train_model(self):
        """
        Train model with sample data
        Features:
        [late_night, high_frequency, unplanned_ratio]
        """

        X = np.array([
            [1, 1, 1],  # high risk
            [1, 0, 1],
            [0, 1, 1],
            [0, 0, 1],
            [0, 0, 0],  # low risk
            [0, 1, 0],
            [1, 1, 0],
            [0, 0, 0]
        ])

        y = np.array([
            1, 1, 1, 0,
            0, 0, 1, 0
        ])

        self.model.fit(X, y)

    def predict_risk(self, features):
        """
        Predict probability
        """
        prob = self.model.predict_proba([features])[0][1]
        return float(prob)
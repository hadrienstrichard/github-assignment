"""Assignment - making a sklearn estimator.

The goal of this assignment is to implement by yourself a scikit-learn
estimator for the OneNearestNeighbor and check that it is working properly.

The nearest neighbor classifier predicts for a point X_i the target y_k of
the training sample X_k which is the closest to X_i. We measure proximity with
the Euclidean distance. The model will be evaluated with the accuracy (average
number of samples corectly classified). You need to implement the `fit`,
`predict` and `score` methods for this class. The code you write should pass
the test we implemented. You can run the tests by calling at the root of the
repo `pytest test_sklearn_questions.py`.

We also ask to respect the pep8 convention: https://pep8.org. This will be
enforced with `flake8`. You can check that there is no flake8 errors by
calling `flake8` at the root of the repo.

Finally, you need to write docstring similar to the one in `numpy_questions`
for the methods you code and for the class. The docstring will be checked using
`pydocstyle` that you can also call at the root of the repo.
"""
import numpy as np
from sklearn.base import BaseEstimator
from sklearn.base import ClassifierMixin
from sklearn.utils.validation import check_X_y
from sklearn.utils.validation import check_array
from sklearn.utils.validation import check_is_fitted
from sklearn.utils.multiclass import check_classification_targets


class OneNearestNeighbor(BaseEstimator, ClassifierMixin):
    """OneNearestNeighbor classifier."""

    def __init__(self):  # noqa: D107
        pass

    def fit(self, X, y):
        """Fit the OneNearestNeighbor classifier.

        Parameters
        ----------
        X : array-like or pd.DataFrame, shape (n_samples, n_features)
            The training input samples.
        y : array-like, shape (n_samples,)
            The target values.

        Returns
        -------
        self : object
            Returns self.
        """
        X, y = check_X_y(X, y)
        check_classification_targets(y)
        self.classes_ = np.unique(y)
        self.n_features_in_ = X.shape[1]

        if len(self.classes_) <= 1:
            raise ValueError(
                "Classifier can't predict when only one class is present."
            )

        self.x_ = X
        self.y_ = y

        return self

    def predict(self, X):
        """Predict the labels for input samples.

        Parameters
        ----------
        X : array-like or pd.DataFrame, shape (n_samples, n_features)
            The input samples.

        Returns
        -------
        y_pred : array, shape (n_samples,)
            The predicted labels for each input sample.
        """
        check_is_fitted(self)
        X = check_array(X)
        y_pred = np.full(
            shape=len(X), fill_value=self.classes_[0],
            dtype=self.classes_.dtype
        )

        # Using broadcasting to compute distances
        train_points_expanded = self.x_[:, np.newaxis, :]
        distances = np.sqrt(np.sum((train_points_expanded - X) ** 2, axis=2)).T

        # Sort the distances and take the k smallest distances
        indices = np.argsort(distances)[:, :1]

        # Take the label mode as the prediction
        y_pred = self.y_[indices]

        return np.squeeze(y_pred)

    def score(self, X, y):
        """Return the accuracy of the model on the given test data and labels.

        Parameters
        ----------
        X : array-like or pd.DataFrame, shape (n_samples, n_features)
            The input samples.
        y : array-like, shape (n_samples,)
            The true labels.

        Returns
        -------
        accuracy : float
            The accuracy of the model.
        """
        X, y = check_X_y(X, y)
        y_pred = self.predict(X)

        # Calculate accuracy
        accuracy = np.mean(y_pred == y)

        return accuracy

from __future__ import annotations

from typing import List

import pandas as pd
from sklearn import linear_model

from model_quality_report.model_base import ModelBase


class LinearModelWrapper(ModelBase):
    def __init__(self, exog_cols: List[str]) -> None:
        self._exog_cols = exog_cols
        self.model = linear_model.LinearRegression()

    def fit(self, X_train: pd.DataFrame, y_train: pd.Series) -> LinearModelWrapper:
        self.model.fit(X_train[self._exog_cols], y_train)
        return self

    def predict(self, X_test: pd.DataFrame) -> pd.Series:
        return pd.Series(
            self.model.predict(X_test[self._exog_cols]), index=X_test.index
        )

# For ShoppingHolidayCalendar class
import holidays
from datetime import date, datetime
from dateutil.relativedelta import relativedelta, TH

# For ShoppingHolidays class
from sklearn.base import BaseEstimator, TransformerMixin
from scipy.sparse import lil_matrix
import numpy as np


# holiday calendar class
# THIS NEEDS MAINTANENCE!
class ShoppingHolidayCalendar(holidays.HolidayBase):
    def __init__(self, country='all', **kwargs):
        super().__init__(**kwargs)
        self.country = country

    def _populate(self, year):
        # Thanksgiving, 4th Thursday of November
        if self.country in ['all', 'US']:
            dt = date(year, 11, 1) \
                + relativedelta(weekday=TH(+4))
            self[dt] = "Thanksgiving"

        # Black Friday, one day after Thanksgiving
        # introduced in the USA in 1952
        if year >= 1952 and self.country in ['all', 'US']:
            dt = date(year, 11, 1) \
                + relativedelta(weekday=TH(+4)) \
                + relativedelta(days=+1)
            self[dt] = "Black Friday (USA)"

        # Cyber Monday, Monday after thanksgiving
        # introduced in the USA in 2005
        if year >= 2005 and self.country in ['all', 'US']:
            dt = date(year, 11, 1) \
                + relativedelta(weekday=TH(+4)) \
                + relativedelta(days=+4)
            self[dt] = "Cyber Monday (USA)"

        # Singles Day (CN), 11th Nov every year
        # started by Nanjing University students in China in 1993
        if year >= 1993 and self.country in ['all', 'CN']:
            self[date(year, 11, 11)] = "Singles Day (CN)"

        # Chinese New Year, if self.country in ['all', 'CN', 'TW']
        # Diwali, India
        # El Buen Fin, Mexico


# Sklearn API
class ShoppingHolidays(BaseEstimator, TransformerMixin):
    def __init__(self, sparse=True, country='all'):
        self.sparse = sparse
        self.calendar = ShoppingHolidayCalendar(country=country)

    def fit(self, X, y=None):
        self.column_names = ['na']
        return self

    def transform(self, X, copy=None):
        # convert to numpy array
        if isinstance(X, (datetime, date)):
            X = [X]
        if isinstance(X, (list, tuple)):
            X = np.array(X)
        if len(X.shape) == 1:
            X = X.reshape(-1, 1)

        n_samples, n_features = X.shape
        Z = lil_matrix((n_samples, n_features), dtype=bool)

        for i in range(n_samples):
            for j in range(n_features):
                if X[i, j] in self.calendar:
                    Z[i, j] = True

        # convert to dense or CSR sparse matrix
        if not self.sparse:
            return Z.toarray()
        else:
            return Z.tocsr()

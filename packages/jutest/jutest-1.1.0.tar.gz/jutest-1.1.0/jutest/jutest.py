import pandas as pd

from jutest.actions.contains import ContainsAction
from jutest.actions.info import InfoAction
from jutest.actions.load import load
from jutest.actions.show_duplicates import show_duplicates
from jutest.actions.show_encodings import show_encodings
from jutest.actions.show_nulls import show_nulls
from jutest.actions.show_outliers import show_outliers
from jutest.actions.show_popularity import show_popularity
from jutest.actions.show_values import show_values
from jutest.encode.checker import EncodeChecker
from jutest.settings import DEFAULT_INFO_PRECISION


class Jutest:
    def __init__(self):
        self.dataframe = pd.DataFrame()
        self.encode_checker = EncodeChecker()

    def load(self, filename: str, show: bool = True, **kwargs):
        """
        Load CSV file
        :param filename: name of CSV file
        :param show: [optional] display result in screen
        :param kwargs: [optional] display options
        """
        self.dataframe = load(filename, show, **kwargs)

    def info(self, precision: int = DEFAULT_INFO_PRECISION):
        """
        Main info about data
        :param precision: [optional] count of digits after dot in min, max, mean, std values
        """
        info_action = InfoAction(self.dataframe, self.encode_checker)
        info_action.info(precision)

    def show_values(self, where: dict, **kwargs):
        """
        Filter rows with `where` values
        :param where: dict were `key` is column name and `value` is column value
        :param kwargs: [optional] display options
        """
        show_values(self.dataframe, where, **kwargs)

    def show_nulls(self, column_name: str = None, **kwargs):
        """
        Show rows where column `column_name` is NaN (or all columns if `column_name` is None)
        :param column_name: [optional] name of filtering column (or None to use all columns)
        :param kwargs: [optional] display options
        """
        show_nulls(self.dataframe, column_name, **kwargs)

    def show_outliers(self, column_name: str, **kwargs):
        """
        Show rows where column `column_name` has outliers
        :param column_name: name of filtering column
        :param kwargs: [optional] display options
        """
        show_outliers(self.dataframe, column_name, **kwargs)

    def show_encodings(self, column_name: str, **kwargs):
        """
        Show rows where column `column_name` has problem with encoding
        :param column_name: name of filtering column
        :param kwargs: [optional] display options
        """
        show_encodings(self.dataframe, self.encode_checker, column_name, **kwargs)

    def show_duplicates(self, column_names: list, limit_groups: int = 5, limit: int = 3, **kwargs):
        """
        Split rows in groups, where columns `column_names` have equal values
        :param column_names: names of filtering columns
        :param limit_groups: [optional] count of groups
        :param limit: [optional] count of rows in each group (display option)
        :param kwargs: [optional] display options
        """
        show_duplicates(self.dataframe, column_names, limit_groups, limit=limit, **kwargs)

    def show_popularity(self, column_name: str, **kwargs):
        """
        Show most popular values of `column_name` with count of this values
        :param column_name: name of filtering column
        :param kwargs: [optional] display options
        """
        show_popularity(self.dataframe, column_name, **kwargs)

    def contains(self, filename: str, column_name: str, **kwargs):
        """
        Check if all values of `column_name` exists in `filename`
        :param filename: name of file with values (each value in new line)
        :param column_name: name of checking column
        :param kwargs: [optional] display options
        """
        contains_action = ContainsAction(filename)
        contains_action.contains(self.dataframe, column_name, **kwargs)

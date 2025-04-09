from typing import List

import kagglehub
import pandas as pd
from kagglehub import KaggleDatasetAdapter

from config import DATASET_FILE, DATASET_NAME


class DataLoader:
    """
    A class to load a Kaggle dataset into a pandas DataFrame and provide methods
    to access data for specific metrics.
    """

    def __init__(
        self,
        dataset_name: str = DATASET_NAME,
        dataset_file: str = DATASET_FILE,
    ):
        """
        Initializes the DataLoader by downloading the dataset (if necessary)
        and loading it into a pandas DataFrame.

        Args:
            dataset_name (str): The name of the Kaggle dataset (e.g., 'username/dataset-name').
            dataset_file (str): The name of the file within the dataset to load (e.g., 'data.csv').
        """

        self.dataset_name = dataset_name
        self.dataset_file = dataset_file
        self.df = self._load_dataframe()

    def _load_dataframe(self) -> pd.DataFrame:
        """
        Loads the dataset file into a pandas DataFrame.

        Returns:
            pd.DataFrame: The loaded DataFrame.
        """

        return kagglehub.load_dataset(
            KaggleDatasetAdapter.PANDAS,
            self.dataset_name,
            self.dataset_file,
            pandas_kwargs={"encoding": "latin-1"},
        )

    def get_data_for_metric(self, columns: List[str]) -> pd.DataFrame:
        """
        Retrieves filtered data.

        Args:
            columns (List[str]): List of columns to filter the DataFrame.

        Returns:
            pd.DataFrame: DataFrame containing data for metric xyz1.
        """

        return self.df[columns].copy()

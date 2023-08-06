from abc import ABC, abstractmethod
from pyspark.sql import DataFrame


class DataFramePrintInterface(ABC):
    @abstractmethod
    def print(self, df: DataFrame):
        pass

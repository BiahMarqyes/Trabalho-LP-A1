import unittest
import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from hipotese_2 import plot_renewable_energy_consumption_continental, plot_renewable_energy_consumption_per_capita
from data_cleaner import
from unittest.mock import patch

class Test(unittest.TestCase):
    def setUp(self):
        self.df = pd.read_csv("data/World Energy Consumption.csv")

if __name__ == "__main__":
    unittest.main()
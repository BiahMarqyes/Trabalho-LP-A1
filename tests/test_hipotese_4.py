from matplotlib.testing.decorators import check_figures_equal
import matplotlib.pyplot as plt
import unittest
import pandas as pd
import numpy as np
import os
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from hipotese_4 import (countries_with_most_na, countries_with_na_counts, 
                         plot_country_energy_gdp, plot_top_9_countries, 
                         plot_lower_9_countries, energy_gdp_correlation)
class TestGDPAndFossilEnergyAnalysis(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'country': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'] * 3,
            'year': [2000, 2001, 2002] * 9,
            'fossil_energy_per_capita': [10, np.nan, 30, 40, 50, 60, 70, 80, 90] * 3,
            'gdp': [1, 2, 3, 4, 5, 6, 7, 8, 9] * 3
        })
        self.colors = ['#003049', '#669bbc']

    def test_countries_with_most_na(self):
        result = countries_with_most_na(self.df, "fossil_energy_per_capita", top_n=2)
        expected = ['B', 'A']
        self.assertEqual(result, expected)

    def test_countries_with_na_counts(self):
        result = countries_with_na_counts(self.df, "fossil_energy_per_capita", top_n=2)
        expected = pd.DataFrame({
            'Country': ['B', 'A'],
            'NA Count': [3, 0]
        })
        pd.testing.assert_frame_equal(result, expected)

if __name__ == "__main__":
    unittest.main()

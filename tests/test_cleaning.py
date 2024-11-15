import unittest
import sys
import os
import pandas as pd
# Adiciona o diretório src ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from data_cleaner import demand_and_production # Importem suas funções aqui!!


class TestCleaning(unittest.TestCase):
    def setUp(self):
        self.df = pd.read_csv("data/World Energy Consumption.csv")


    # Testes da Hipótese 1


    # Testes da Hipótese 2


    # Testes da Hipótese 3
    def test_non_country_removal(self):
        df_clean = demand_and_production(self.df)
        # Confirma se os não países foram removidos
        non_countries = [
            'ASEAN (Ember)', 'Africa', 'Asia', 'OPEC (EI)'
        ]
        self.assertFalse(df_clean['country'].isin(non_countries).any())

    def test_column_selection(self):
        df_clean = demand_and_production(self.df)
        # Confirma se o DataFrame resultante contém apenas as colunas esperadas
        expected_columns = ['country', 'year', 'gdp', 'electricity_demand', 'renewables_electricity']
        self.assertListEqual(list(df_clean.columns), expected_columns)

    def test_null_value_removal(self):
        df_clean = demand_and_production(self.df)
        # Confirma se não há valores nulos em 'electricity_demand' e 'renewables_electricity'
        self.assertFalse(df_clean[['electricity_demand', 'renewables_electricity']].isnull().any().any())

    def test_year_filtering(self):
        df_clean = demand_and_production(self.df)
        # Confirma se os anos estão entre 2000 e 2021
        self.assertTrue((df_clean['year'] >= 2000).all() and (df_clean['year'] <= 2021).all())


    # Testes da Hipótese 4


if __name__ == '__main__':
    unittest.main()

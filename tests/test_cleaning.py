import unittest
import sys
import os
import pandas as pd
import numpy as np

# Adiciona o diretório src ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from data_cleaner import demand_and_production, GDP_and_fossil_energy_consumption, continent_identifier, renewable_energy_consumption_by_continent # Importem suas funções aqui!!


class TestCleaning(unittest.TestCase):
    def setUp(self):
        self.df = pd.read_csv("../data/World Energy Consumption.csv")


    # Testes da Hipótese 1
    def test_hipotese_1_column_selection_consumption_and_population(self):
        df_clean = consumption_and_population(self.df)
        # Confirma se o DataFrame resultante contém apenas as colunas esperadas
        expected_columns = ["country", "year", "population", "primary_energy_consumption"]
        self.assertListEqual(list(df_clean.columns), expected_columns)
        
    def test_hipotese_1_column_selection_electricity_balance_and_import(self):
            df_clean = consumption_and_population(self.df)
            # Confirma se o DataFrame resultante contém apenas as colunas esperadas
            expected_columns = ["year","electricity_balance","net_elec_imports"]
            self.assertListEqual(list(df_clean.columns), expected_columns)
        
    def test_hipotese_1_column_selection_electricity_demand_and_import(self):
            df_clean = consumption_and_population(self.df)
            # Confirma se o DataFrame resultante contém apenas as colunas esperadas
            expected_columns = ["year","electricity_demand","net_elec_imports"]
            self.assertListEqual(list(df_clean.columns), expected_columns)
        
    def test_hipotese_1_null_value_removal(self):
            df_clean = consumption_and_population(self.df)
            # Confirma se não há valores nulos em 'population' e 'primary_energy_consumption'
            self.assertFalse(df_clean[["population", "primary_energy_consumption"]].isnull().any().any())
        
            df_clean = electricity_balance_and_import(self.df)
            # Confirma se não há valores nulos em 'electricity_balance' e 'net_elec_imports'
            self.assertFalse(df_clean[["electricity_balance", "net_elec_imports"]].isnull().any().any())
        
            df_clean = electricity_demand_and_import(self.df)
            # Confirma se não há valores nulos em 'electricity_demand' e 'net_elec_imports'
            self.assertFalse(df_clean[["electricity_demand", "net_elec_imports"]].isnull().any().any())
        
    def test_hipotese_1_year_filtering(self):
            df_clean = electricity_demand_and_import(self.df)
            # Confirma se os anos estão entre 2000 e 2020
            self.assertTrue((df_clean['year'] >= 2000).all() and (df_clean['year'] <= 2020).all())

    # Testes da Hipótese 2
    
    def test_continent_identifier(self):    
        try:
            # Países válidos
            self.assertEqual(continent_identifier("Brazil"), "South America")
            self.assertEqual(continent_identifier("Australia"), "Oceania")
            self.assertEqual(continent_identifier("India"), "Asia")
            # "País" inválido
            self.assertIsNone(continent_identifier("G20 (Ember)"))
        except AssertionError as e:
            print(f"Erro no teste: {e}")
            raise

    def test_remocao_dados_consumo_invalidos(self):
        df = renewable_energy_consumption_by_continent(self.df)
        # Confirma se não tem valores nulos nos dados de consumo de energia
        self.assertEqual(df["biofuel_consumption"].isna().sum(), 0)
        self.assertEqual(df["solar_consumption"].isna().sum(), 0)
        self.assertEqual(df["wind_consumption"].isna().sum(), 0)

    def test_remocao_sem_populacao(self):
        df = renewable_energy_consumption_by_continent(self.df)
        # Confirma se os países sem população foram removidos
        self.assertTrue(df["population"].notna().all())

    def test_intervalo_anos(self):
        df = renewable_energy_consumption_by_continent(self.df)
        # Confirma se os anos estão entre 2001 e 2021
        self.assertTrue(all(df["year"].between(2001, 2021)))

    def test_colunas(self):
        df = renewable_energy_consumption_by_continent(self.df)
        # Confirma se o DataFrame resultante contém apenas as colunas esperadas
        self.assertListEqual(list(df.columns), ["continent", "year", "population", "biofuel_consumption", "hydro_consumption", 
        "other_renewable_consumption", "renewables_consumption", "solar_consumption", "wind_consumption", "energy_per_capita", "total_renewable_consumption"])

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


class TestGDPAndFossilEnergyConsumption(unittest.TestCase):
    
    def setUp(self):
        # Configuração de DataFrames de teste
        self.df_complete = pd.DataFrame({
            'country': ['CountryA', 'CountryA', 'CountryB', 'CountryC', 'CountryD'],
            'year': [2000, 2001, 2000, 2000, 2000],
            'gdp': [1000, 1100, 2000, 3000, np.nan],
            'coal_cons_per_capita': [50, 55, 60, 65, 70],
            'fossil_energy_per_capita': [100, 110, 120, 130, np.nan],
            'gas_energy_per_capita': [20, 25, 30, 35, np.nan],
            'oil_energy_per_capita': [30, 35, 40, 45, np.nan]
        })
        
        self.df_missing_gdp = pd.DataFrame({
            'country': ['CountryA', 'CountryB', 'CountryB', 'CountryC', 'CountryC'],
            'year': [2000, 2000, 2001, 2000, 2001],
            'gdp': [1000, np.nan, np.nan, 3000, 3100],
            'coal_cons_per_capita': [50, 60, 65, np.nan, 75],
            'fossil_energy_per_capita': [100, 120, np.nan, 130, 140],
            'gas_energy_per_capita': [20, 30, np.nan, 35, 45],
            'oil_energy_per_capita': [30, 40, np.nan, 45, 50]
        })
        
        self.df_all_missing_gdp = pd.DataFrame({
            'country': ['CountryA', 'CountryA', 'CountryB', 'CountryB'],
            'year': [2000, 2001, 2000, 2001],
            'gdp': [np.nan, np.nan, np.nan, np.nan],
            'coal_cons_per_capita': [50, 55, 60, 65],
            'fossil_energy_per_capita': [100, 110, 120, 130],
            'gas_energy_per_capita': [20, 25, 30, 35],
            'oil_energy_per_capita': [30, 35, 40, 45]
        })

    def test_complete_data(self):
        # Testa com todos os dados preenchidos
        result = GDP_and_fossil_energy_consumption(self.df_complete)
        self.assertEqual(len(result), 4)
        self.assertNotIn('CountryD', result['country'].unique())

    def test_missing_gdp(self):
        # Testa remoção de países com GDP ausente em todos os anos
        result = GDP_and_fossil_energy_consumption(self.df_missing_gdp)
        self.assertEqual(len(result), 3)  # Atualizado para refletir o total correto
        self.assertNotIn('CountryB', result['country'].unique())
        self.assertIn('CountryA', result['country'].unique())
        self.assertIn('CountryC', result['country'].unique())

    def test_all_missing_gdp(self):
        # Testa remoção quando todos os países possuem GDP ausente
        result = GDP_and_fossil_energy_consumption(self.df_all_missing_gdp)
        self.assertTrue(result.empty)

    def test_removal_of_null_rows(self):
        # Testa se linhas com todos os valores de consumo de energia nulos são removidas
        df_with_nulls = self.df_complete.copy()
        df_with_nulls.loc[4, ['coal_cons_per_capita', 'fossil_energy_per_capita', 'gas_energy_per_capita', 'oil_energy_per_capita']] = [np.nan, np.nan, np.nan, np.nan]
        result = GDP_and_fossil_energy_consumption(df_with_nulls)
        self.assertEqual(len(result), 4)

    def test_output_structure(self):
        # Testa a estrutura do DataFrame retornado
        result = GDP_and_fossil_energy_consumption(self.df_complete)
        expected_columns = ['country', 'year', 'gdp', 'coal_cons_per_capita', 'fossil_energy_per_capita', 'gas_energy_per_capita', 'oil_energy_per_capita']
        self.assertListEqual(list(result.columns), expected_columns)
        
if __name__ == '__main__':
    unittest.main()

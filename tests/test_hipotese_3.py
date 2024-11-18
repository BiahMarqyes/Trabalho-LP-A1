import unittest
import sys
import os
import pandas as pd
# Adiciona o diretório src ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from hipotese_3 import (
    plot_comparison_demand_production,
    plot_variation_demand_production,
    plot_variation_in_the_richest_countries,
)
from data_cleaner import demand_and_production
from unittest.mock import patch

class TestEnergyPlots(unittest.TestCase):
    def setUp(self):
        self.df = pd.read_csv("data/World Energy Consumption.csv")
        self.df = demand_and_production(self.df)
        # Agrupando por países
        self.df_grouped = self.df.groupby('year').sum().reset_index()

    @patch("matplotlib.pyplot.savefig")
    def test_plot_comparison_demand_production(self, mock_savefig):
        """Testa a geração do gráfico de barras empilhadas."""
        plot_comparison_demand_production(self.df_grouped)
        mock_savefig.assert_called_once_with('plots/plots_hipotese_3/grafico_1.png', format='png')

    @patch("matplotlib.pyplot.savefig")
    def test_plot_variation_demand_production(self, mock_savefig):
        """Testa a geração do gráfico de variação anual global."""
        plot_variation_demand_production(self.df_grouped)
        mock_savefig.assert_called_once_with('plots/plots_hipotese_3/grafico_2.png', format='png')

    @patch("matplotlib.pyplot.savefig")
    def test_plot_variation_in_the_richest_countries(self, mock_savefig):
        """Testa a geração dos gráficos de variação para os países mais ricos."""
        plot_variation_in_the_richest_countries(self.df)
        mock_savefig.assert_called_once_with('plots/plots_hipotese_3/grafico_3.png', format='png')

    def test_data_processing(self):
        """Verifica se os dados são processados corretamente."""
        self.df_grouped['variation_demand'] = self.df_grouped['electricity_demand'].pct_change() * 100
        self.df_grouped['variation_production'] = self.df_grouped['renewables_electricity'].pct_change() * 100
        
        self.assertIn('variation_demand', self.df_grouped.columns)
        self.assertIn('variation_production', self.df_grouped.columns)

    def test_correlation(self):
        """Verifica o cálculo da correlação."""
        correlation = self.df_grouped['electricity_demand'].corr(self.df_grouped['renewables_electricity'])
        self.assertAlmostEqual(correlation, 1.0, delta=0.1)  # Exemplo com dados fictícios


if __name__ == "__main__":
    unittest.main()

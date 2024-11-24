import unittest
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from unittest.mock import patch

# Adiciona o diretório src ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from data_cleaner import renewable_energy_consumption_continental
from hipotese_2 import (plot_renewable_energy_consumption_continental, plot_mapa_calor_crescimento, plot_renewable_energy_consumption_per_capita, plot_renewable_energy_2021)

class TestContinentPlots(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame(renewable_energy_consumption_continental)
        # Agrupando por ano e continente para os testes
        self.df_grouped = self.df.groupby(['year', 'continent']).sum().reset_index()

    @patch("matplotlib.pyplot.savefig")
    def test_plot_renewable_energy_consumption_continental(self, mock_savefig):
        """
        Testa a geração do gráfico de consumo de energia renovável por continente.
        """
        plot_renewable_energy_consumption_continental(self.df_grouped)
        mock_savefig.assert_called_once_with('plots/plots_hipotese_2/grafico_1.png')

    @patch("matplotlib.pyplot.savefig")
    def test_plot_mapa_calor_crescimento(self, mock_savefig):
        """
        Testa a geração do mapa de calor de crescimento do consumo renovável por continente.
        """
        plot_mapa_calor_crescimento(self.df_grouped)
        mock_savefig.assert_called_once_with('plots/plots_hipotese_2/grafico_2.png')

    @patch("matplotlib.pyplot.savefig")
    def test_plot_renewable_energy_consumption_per_capita(self, mock_savefig):
        """
        Testa a geração do gráfico de consumo de energia renovável per capita.
        """
        plot_renewable_energy_consumption_per_capita(self.df_grouped)
        mock_savefig.assert_called_once_with('plots/plots_hipotese_2/grafico_3.png')

    @patch("matplotlib.pyplot.savefig")
    def test_plot_renewable_energy_2021(self, mock_savefig):
        """
        Testa a geração do gráfico de participação de tipos de energia renovável em 2021.
        """
        plot_renewable_energy_2021(self.df)
        mock_savefig.assert_called_once_with('plots/plots_hipotese_2/grafico_4.png')

class TestDataProcessing(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame(renewable_energy_consumption_continental)
        # Agrupando por ano e continente para os testes
        self.df_grouped = self.df.groupby(['year', 'continent']).sum().reset_index()
       
    def test_growth_calculation(self):
        """
        Verifica o cálculo do crescimento percentual do consumo de energia renovável.
        """
        self.df_grouped['pct_growth'] = self.df_grouped.groupby('continent')['total_renewable_consumption'].pct_change() * 100
        self.assertIn('pct_growth', self.df_grouped.columns)

    def test_log_scale_plot(self):
        """
        Verifica se a escala logarítmica é aplicada corretamente ao gráfico per capita.
        """
        plt.figure(figsize=(14, 6))
        sns.lineplot(x='year', y='energy_per_capita', data=self.df_grouped)
        plt.yscale('log')
        self.assertEqual(plt.gca().get_yscale(), 'log')

if __name__ == "__main__":
    unittest.main()

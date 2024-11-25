"""Testes da Hipótese 1"""
import unittest
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from data_cleaner import (consumption_and_population, electricity_balance_and_import, electricity_demand_and_import)
from hipotese_1 import (plot_consumption_population, plot_electricity_balance_import, plot_electricity_demand_import)


class TestHipotese1(unittest.TestCase):
    def test_line_graphs_consumption_population(self, mock_savefig):
        """
        Testa a geração do gráfico de linha do consumo de energia e da população.
        """
        plot_consumption_population(self.df_grouped)
        mock_savefig.assert_called_once_with('plots/plots_hipotese_1/Line_graphs_consumption_population.png')
    
    @patch("matplotlib.pyplot.savefig")
    
    def test_scatter_plot_consumption_population(self, mock_savefig):
        """
        Testa a geração do gráfico de dispersão do consumo de energia e da população.
        """
        plot_consumption_population(self.df_grouped)
        mock_savefig.assert_called_once_with('plots/plots_hipotese_1/Scatter_plot_consumption_population.png')
    
    @patch("matplotlib.pyplot.savefig")
    
    def test_line_graphs_electricity_balance_import(self, mock_savefig):
        """
        Testa a geração do gráfico de linha do balanço de eletricidade e da importação.
        """
        plot_electricity_balance_import(self.df_grouped)
        mock_savefig.assert_called_once_with('plots/plots_hipotese_1/Line_graphs_electricity_balance_import.png')
    
    @patch("matplotlib.pyplot.savefig")
    
    def test_scatter_plot_electricity_balance_import(self, mock_savefig):
        """
        Testa a geração do gráfico de dispersão do balanço de eletricidade e da importação.
        """
        plot_electricity_balance_import(self.df_grouped)
        mock_savefig.assert_called_once_with('plots/plots_hipotese_1/Scatter_plot_electricity_balance_import.png')
    
    @patch("matplotlib.pyplot.savefig")
    
    def test_line_graphs_electricity_demand_import(self, mock_savefig):
        """
        Testa a geração do gráfico de linha da demanda de eletricidade e da importação.
        """
        plot_electricity_demand_import(self.df_grouped)
        mock_savefig.assert_called_once_with('plots/plots_hipotese_1/Line_graphs_electricity_demand_import.png')
    
    @patch("matplotlib.pyplot.savefig")
    
    def test_scatter_plot_electricity_demand_import(self, mock_savefig):
        """
        Testa a geração do gráfico de dispersão da demanda de eletricidade e da importação.
        """
        plot_electricity_demand_import(self.df_grouped)
        mock_savefig.assert_called_once_with('plots/plots_hipotese_1/Scatter_plot_electricity_demand_import.png')
    

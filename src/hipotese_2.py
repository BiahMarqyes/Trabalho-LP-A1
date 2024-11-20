"""
Módulo responsável por gerar gráficos sobre a hipotése de consumo por continentes
"""

import pandas as pd
import matplotlib.pyplot as plt
import data_cleaner
import seaborn as sns
# import numpy as np

df = pd.DataFrame(data_cleaner.renewable_energy_consumption_continental)

# Cria uma nova coluna no novo DF com a soma dos diferentes tipos de energia renovável
df['total_renewable_consumption'] = (
    df['biofuel_consumption'] +
    df['hydro_consumption'] +
    df['other_renewable_consumption'] +
    df['renewables_consumption'] +
    df['solar_consumption'] +
    df['wind_consumption']
)

df['renewable_consumption_per_capita'] = df['total_renewable_consumption'] / df['population']

def plot_renewable_energy_consumption_continental(df: pd.DataFrame) -> None:
    """
    Plota um gráfico de linhas com o consumo de energia renovável por continente ao longo dos anos.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame com os dados usados.
    """
    # Agrupa os dados por ano e continente
    grouped_data = df.groupby(['year', 'continent'])['total_renewable_consumption'].sum().reset_index()

    # Estilo do gráfico
    plt.figure(figsize=(15, 7))

    # Plota gráfico de linhas
    sns.lineplot(
        x='year', y='total_renewable_consumption', data=grouped_data,
        hue='continent', palette='Blues', linewidth=3
    )

    # Intervalos do eixo X
    intervalos_x = list(range(2000, 2023))
    plt.xticks(intervalos_x, [str(x) for x in intervalos_x])

    # Título e rótulos
    plt.title('Consumo Global de Energia Renovável por Continente (2000-2022)', fontsize=17, pad=20)
    plt.xlabel('Ano', fontsize=12)
    plt.ylabel('Consumo de Energia (Terrawatt Hour)', fontsize=12)

    # Adiciona a legenda
    plt.legend(title='Continente', fontsize=11)

    # Estiliza o gráfico
    sns.despine()

    # Salva gráfico
    plt.savefig('./plots/plots_hipotese_2/grafico_1.png', format='png')
    plt.show()
    plt.close()


plot_renewable_energy_consumption_continental(df)


def plot_renewable_energy_consumption_per_capita(df: pd.DataFrame) -> None:
    """
    Plota um gráfico de linhas com o consumo total de energia renovável per capita por continente ao longo dos anos.

    Parameters
    ----------
    df : pd.DataFrame
        O DataFrame com os dados dos continentes.
    """
    # Agrupa os dados por ano e continente
    grouped_data = df.groupby(['year', 'continent'])['renewable_consumption_per_capita'].sum().reset_index()

    # Tamanho do gráfico
    plt.figure(figsize=(15, 7))

    # Plota gráfico de linhas com diferentes continentes
    sns.lineplot(
        x='year', y='renewable_consumption_per_capita', data=grouped_data,
        hue='continent', palette='Blues', linewidth=3
    )

    # Configurando o gráfico
    intervalos_x = list(range(2000, 2023))
    plt.xticks(intervalos_x, [str(x) for x in intervalos_x])

    plt.title('Consumo Global de Energia Renovável per Capita (2000-2022)', fontsize=17, pad=20)
    plt.xlabel('Ano', fontsize=12)
    plt.ylabel('Consumo de Energia per Capita (Terrawatt Hour)', fontsize=12)

    plt.legend(title='Continente', fontsize=11)

    sns.despine()

    # Salva gráfico
    plt.savefig('./plots/plots_hipotese_2/grafico_2.png')
    plt.show()
    plt.close()

plot_renewable_energy_consumption_per_capita(df)
"""
Módulo responsável por gerar gráficos sobre a hipotése de consumo por continentes
"""

import pandas as pd
import matplotlib.pyplot as plt
import data_cleaner
import seaborn as sns

df = pd.DataFrame(data_cleaner.renewable_energy_consumption_continental)

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

    # Calcula a média global por ano
    global_mean = grouped_data.groupby('year')['total_renewable_consumption'].mean().reset_index()
    global_mean['continent'] = 'Global'

    # Tamanho do gráfico
    plt.figure(figsize=(15, 7))

    # Paleta de cores para os continentes
    continents = grouped_data['continent'].unique().tolist()
    palette = sns.color_palette('Dark2', n_colors=len(continents))

    # Congigura gráfico de linhas
    ax = sns.lineplot(
        x='year', y='total_renewable_consumption', data=grouped_data,
        hue='continent', palette=palette, linewidth=2.5
    )
        
    # Coloca os nomes dos continentes diretamente nas linhas
    for i, continent in enumerate(continents):
        subset = grouped_data[grouped_data['continent'] == continent]
        plt.text(
            x=subset['year'].iloc[-1] + 0.2, 
            y=subset['total_renewable_consumption'].iloc[-1],
            s=continent, 
            fontsize=11, 
            color=palette[i]
        )
      
    # Plota a linha da média global
    plt.plot(
        global_mean['year'], global_mean['total_renewable_consumption'], 
        color='gray', linestyle='--', linewidth=1.5, label='Média Global'
    )
      
    # Rótulo da média
    plt.text(
        x=global_mean['year'].iloc[-1] + 0.2, 
        y=global_mean['total_renewable_consumption'].iloc[-1],
        s='Global Average', 
        fontsize=11, 
        color='gray'
    )

    # Ajusta o gráfico para melhor visualização dos dados de 2001 a 2021
    plt.xlim(grouped_data['year'].min(), grouped_data['year'].max())

    # Define a escala dos anos no eixo x
    plt.xticks(list(range(2001, 2022, 2)))

    # Títulos e rótulos
    plt.title('Consumo Global de Energia Renovável por Continente (2001-2021)', fontsize=17, pad=20)
    plt.xlabel('')
    plt.ylabel('Consumo\nde\n Energia\n(Terrawatt\nHour)', fontsize=12, rotation = 0, labelpad=30, ha='center')

    # Remove grades desnecessárias e legenda
    sns.despine()
    ax.get_legend().remove()

    # Salva o gráfico
    plt.savefig('../plots/plots_hipotese_2/grafico_1.png')

plot_renewable_energy_consumption_continental(df)

def plot_mapa_calor_crescimento(df: pd.DataFrame) -> None:
    """
    Cria um mapa de calor para visualizar o crescimento percentual do consumo de energia renovável 
    por continente ao longo dos anos.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame com os dados usados.
    """

    # Agrupa os dados por ano e continente
    grouped_data = df.groupby(['year', 'continent'])['total_renewable_consumption'].sum().reset_index()

    # Calcula o crescimento percentual ano a ano para cada continente
    grouped_data['pct_growth'] = grouped_data.groupby('continent')['total_renewable_consumption'].pct_change() * 100

    # Converte os dados para formato de tabela
    heatmap_data = grouped_data.pivot(index='continent', columns='year', values='pct_growth')

    # Elimina valores nulos
    heatmap_data.fillna(0, inplace=True)

    # Tamanho do gráfico
    plt.figure(figsize=(15, 7))

    # Cria um mapa de calor, com paleta, configurações de rótulos e linhas
    sns.heatmap(
        heatmap_data, cmap='coolwarm_r', annot=True, fmt=".1f", linewidths=.5, 
        cbar_kws={'label': 'Crescimento (%)'}, linecolor='gray'
    )

    # Títulos e rótulos
    plt.title('Mapa de Calor do Crescimento do Consumo de Energia Renovável (2001-2021)', fontsize=17, pad=20)
    plt.xlabel('')
    plt.ylabel('Continente', fontsize=12)

    plt.savefig('../plots/plots_hipotese_2/grafico_2.png')

plot_mapa_calor_crescimento(df)

def plot_renewable_energy_consumption_per_capita(df: pd.DataFrame) -> None:
    """
    Plota um gráfico de linhas com o consumo total de energia renovável per capita por continente em escala logarítmica.

    Parameters
    ----------
    df : pd.DataFrame
        O DataFrame com os dados dos continentes.
    """
    # Agrupa os dados por ano e continente
    grouped_data = df.groupby(['year', 'continent'])['energy_per_capita'].sum().reset_index()

    # Tamanho do gráfico
    plt.figure(figsize=(14, 6))

    # Paleta de cores para os continentes
    continents = grouped_data['continent'].unique().tolist()
    palette = sns.color_palette('Dark2', n_colors=len(continents))

    # Configura o gráfico de linhas
    ax = sns.lineplot(
        x='year', y='energy_per_capita', data=grouped_data,
        hue='continent', linewidth=2.5, palette=palette
        )

    # Legenda diretamente nas linhas
    for i, continent in enumerate(continents):
        subset = grouped_data[grouped_data['continent'] == continent]
        plt.text(
            x=subset['year'].iloc[-1] + 0.2, 
            y=subset['energy_per_capita'].iloc[-1],
            s=continent, 
            fontsize=11, 
            color=palette[i]
        )

    # Ajusta o gráfico para melhor visualização dos dados de 2001 a 2021
    plt.xlim(grouped_data['year'].min(), grouped_data['year'].max())

    # Escala logarítmica no eixo y
    plt.yscale('log')

    # Define a escala dos anos no eixo x
    plt.xticks(list(range(2001, 2022, 2)))

    # Títulos e rótulos
    plt.title('Consumo Global de Energia Renovável per Capita (2001-2021)', fontsize=17, pad=20)
    plt.xlabel('')
    plt.ylabel('Consumo de\nEnergia\nper Capita\n(log)', fontsize=12, rotation=0, labelpad=50, ha='center')

    # Limpa estilo
    sns.despine()
    ax.get_legend().remove()

    plt.savefig('../plots/plots_hipotese_2/grafico_3.png')

plot_renewable_energy_consumption_per_capita(df)


def plot_renewable_energy_2021(df: pd.DataFrame) -> None:
    """
    Plota um gráfico de barras empilhadas para mostrar a participação de cada tipo de energia renovável
    por continente no ano de 2021.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame com os dados usados.
    """
    # Filtra os dados para o ano de 2021
    data_2021 = df[df['year'] == 2021]

    # Agrupa os dados por continente e calcula o consumo total por tipo de energia em 2021
    grouped_data = data_2021.groupby('continent')[['biofuel_consumption', 'hydro_consumption', 'other_renewable_consumption', 'solar_consumption', 'wind_consumption']].sum()

    # Calcula a % de cada tipo de energia
    share_data = grouped_data.div(grouped_data.sum(axis=1), axis=0) * 100

    # Cria o gráfico de barras empilhadas horizontais
    share_data = share_data.plot(
        kind='barh', 
        stacked=True, 
        figsize=(15, 8), 
        color=sns.color_palette('Dark2', n_colors=share_data.shape[1])
    )

    # Adiciona títulos e rótulos
    plt.title('Participação de Cada Tipo de Energia Renovável por Continente (2021)', fontsize=17, pad=20)
    plt.ylabel('Continente', fontsize=12)
    plt.xlabel('Participação (%)', fontsize=12)

    # Localiza a legenda
    legend_labels = ['Biofóssil', 'Hidrelétrica', 'Outras Renováveis', 'Solar', 'Eólica']
    plt.legend(title='Tipo de Energia', labels=legend_labels, bbox_to_anchor=(0.95, 0.61))

    # Limpeza
    sns.despine()

    # Exibe o gráfico
    plt.savefig('../plots/plots_hipotese_2/grafico_4.png')

plot_renewable_energy_2021(df)

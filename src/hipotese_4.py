"""
Módulo para as análises da relação entre PIB e consumo de Energia Fóssil
"""
import numpy as np
import data_cleaner
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


df = pd.DataFrame(data_cleaner.GDP_and_fossil_energy_frame)


df_auxiliary = df.set_index(['country', 'year'])


print(df.index)
columns = df.columns

# Lista de paises com muitos valores nulos
def countries_with_most_na(df, column, top_n=10):
    
  
# Tabela para visualizar quantidade de valores nulos
    """
    Retorna uma lista dos países com mais valores NA em uma coluna específica.

    Parameters
    ----------
    df : DataFrame
        DataFrame com os dados.
    column : str
        Nome da coluna para verificar valores NA.
    top_n : int, optional
        Número de países a retornar (padrão é 10).

    Returns
    -------
    List[str]
        Lista de países com mais valores NA na coluna especificada, em ordem decrescente.
    """
    
    # Calcular o número de valores NA por país na coluna especificada
    na_counts = df.groupby('country')[column].apply(lambda x: x.isna().sum())
    
    # Ordenar os países pelo número de valores NA em ordem decrescente e pegar os top_n
    top_countries_with_na = na_counts.sort_values(ascending=False).head(top_n).index.tolist()
    
    return top_countries_with_na
def countries_with_na_counts(df, column, top_n=10):
    """
    Retorna os países com mais valores NA em uma coluna específica, junto com a quantidade de valores NA.

    Parameters
    ----------
    df : DataFrame
        DataFrame com os dados.
    column : str
        Nome da coluna para verificar valores NA.
    top_n : int, optional
        Número de países a retornar (padrão é 10).

    Returns
    -------
    DataFrame
        DataFrame com os países e suas contagens de valores NA na coluna especificada, em ordem decrescente.
    """
    
    # Calcular o número de valores NA por país na coluna especificada
    na_counts = df.groupby('country')[column].apply(lambda x: x.isna().sum())
    
    # Ordenar pelo número de valores NA em ordem decrescente e pegar os top_n
    top_countries_with_na = na_counts.sort_values(ascending=False).head(top_n)
    
    # Converter para DataFrame
    result_df = top_countries_with_na.reset_index()
    result_df.columns = ['Country', 'NA Count']
    
    return result_df


na_countries = countries_with_most_na(df, "fossil_energy_per_capita",6)

#print(countries_with_na_counts(df, "fossil_energy_per_capita", 6))

for country in na_countries:
    df_auxiliary = df_auxiliary.drop(country)
    
# o Sri Lanka e outros foram removidos pois não possuem dados suficientes de consumo para serem representativos




# Função que plota o gráfico de cada país 
def plot_country_energy_gdp(df, country, ax, column, colors):
    """
    Plota o consumo de energia fóssil e o PIB para um determinado país ao longo do tempo.

    Parameters
    ----------
    df : DataFrame
        DataFrame com os dados de energia e PIB.
    country : str
        Nome do país a ser plotado.
    ax : matplotlib.axes.Axes
        Eixo para plotar o gráfico de consumo de energia fóssil.
    column : str
        Coluna do DataFrame que representa o consumo de energia fóssil per capita.
    colors : list
        Lista de cores para o gráfico. A primeira cor será usada para o consumo de energia, 
        e a segunda cor será usada para o PIB.

    Returns
    -------
    None.
        A função plota o gráfico, sem retornar valores.
    """
    paises_selecionados = df.loc[country]
    
    # Gráfico de linhas para o consumo de energia fóssil
    sns.lineplot(data=paises_selecionados, x=paises_selecionados.index.get_level_values('year'),
                 y=column, marker=None, linestyle='solid', ax=ax, color=colors[0], label='Energia Fóssil', linewidth=3)
    
    # Gráfico de linhas para o PIB em um outro eixo
    ax2 = ax.twinx()
    sns.lineplot(data=paises_selecionados, x=paises_selecionados.index.get_level_values('year'),
                 y='gdp', marker=None, linestyle='solid', ax=ax2, color=colors[1], label='PIB', linewidth=3)

    # Configurações dos eixos
    ax.set_title(f'{country}', fontsize=15, pad=10)
    ax.set_ylabel(None)
    ax2.set_ylabel('PIB', fontsize=14)
    ax.set_xlabel('Ano', fontsize=14)

    ax.tick_params(axis='y', labelsize=13, rotation=0)
    ax2.tick_params(axis='y', labelsize=12, rotation=0)
    

    energia_handle = ax.get_legend_handles_labels()[0][0]
    pib_handle = ax2.get_legend_handles_labels()[0][0]


    # Adicionar as legendas
    
    ax.legend(handles=[energia_handle], labels=['Energia Fóssil'], loc='upper left', 
              fontsize=12, title_fontsize=14, frameon=True, bbox_to_anchor=(0, 1))

    ax2.legend(handles=[pib_handle], labels=['PIB'], loc='upper left', 
               fontsize=12, title_fontsize=14, frameon=True, bbox_to_anchor=(0.02, 0.9))
    
    
    
# Função para plotar os 9 países com maior consumo de energia fóssil
def plot_top_9_countries(df):
    """
    Plota um grid 3x3 dos 9 países com maior consumo médio de energia fóssil per capita.

    Parameters
    ----------
    df : DataFrame
        DataFrame com os dados de energia e PIB, agrupados por país e ano.

    Returns
    -------
    None.
        O gráfico é salvo como um arquivo PNG no diretório '../plots/'.
    """


    # Calculo da média de consumo de energia fóssil per capita de cada país
    media_consumo = df.groupby('country')['fossil_energy_per_capita'].mean()

    # Selecionar os 9 países com o maior consumo médio
    top_9_countries = media_consumo.nlargest(9).index

    # Criar o grid de gráficos (3x3)
    fig, axes = plt.subplots(3, 3, figsize=(20, 12), sharex=True, sharey=False)

    colors = ['#003049', '#669bbc']
    
    for i, country in enumerate(top_9_countries):
        ax = axes[i // 3, i % 3]
        plot_country_energy_gdp(df, country, ax, 'fossil_energy_per_capita', colors)
    
        #ajustes
        ax.legend(loc='upper left', bbox_to_anchor=(0.02, 1.02), fontsize=10)
        ax.tick_params(axis='x', labelsize=13, rotation=45)
        
    fig.text(0, 0.5, 'Consumo de Energia Fóssil per capita',
        va='center', ha='center', rotation='vertical', fontsize=17)
    

    fig.subplots_adjust(top=0.85)

    fig.suptitle(
        'Consumo de Energia Fóssil e PIB dos 9 Países\ncom Maior Consumo Médio de Energia Fóssil',
        fontsize=18, y=0.98)
    
    # Ajustar espaçamento entre os subplots
    fig.tight_layout(pad=3.0, h_pad=3.0, w_pad=3.0)
    
    plt.savefig('../plots/plots_hipotese_4/top_9_countries.png', dpi=300, format='png')
    plt.show()
    plt.close()







# Função para plotar os 9 países com menor consumo de energia fóssil
def plot_lower_9_countries(df):
    """
    Plota um grid 3x3 dos 9 países com menor consumo médio de energia fóssil per capita.

    Parameters
    ----------
    df : DataFrame
        DataFrame com os dados de energia e PIB, agrupados por país e ano.

    Returns
    -------
    None.
        O gráfico é salvo como um arquivo PNG no diretório '../plots/'.
    """
    
    # Calculo da média de consumo de energia fóssil per capita para cada país
    media_consumo = df.groupby('country')['fossil_energy_per_capita'].mean()

    # Selecionar os 9 países com o menor consumo médio
    lower_9_countries = media_consumo.nsmallest(9).index

    # Criar o grid de gráficos (3x3)
    fig, axes = plt.subplots(3, 3, figsize=(20, 12), sharex=True, sharey=False)

    colors = ['brown', 'orange']
    
    for i, country in enumerate(lower_9_countries):
        ax = axes[i // 3, i % 3]
        plot_country_energy_gdp(df, country, ax, 'fossil_energy_per_capita', colors)
        
        # Ajustes
        ax.legend(loc='upper left', bbox_to_anchor=(0.02, 1.02), fontsize=10)
        ax.tick_params(axis='x', labelsize=13, rotation=45)
    
    
    fig.text(0, 0.5, 'Consumo de Energia Fóssil per capita',
        va='center', ha='center', rotation='vertical', fontsize=17)
    
    fig.subplots_adjust(top=0.85)
    fig.suptitle(
        'Consumo de Energia Fóssil e PIB dos 9 Países\ncom Menor Consumo Médio de Energia Fóssil',
        fontsize=18, y=0.98)
    
    # Ajustar espaçamento entre os subplots
    fig.tight_layout(pad=3.0, h_pad=3.0, w_pad=3.0)
    

    plt.savefig('../plots/plots_hipotese_4/lower_9_countries.png', dpi=300, format='png')
    plt.show()
    plt.close()

    
    
plot_top_9_countries(df_auxiliary)
plot_lower_9_countries(df_auxiliary)



def energy_gdp_correlation(df):
    """
    Calcula e plota as contagens de países classificados por níveis de correlação (alta, moderada e baixa) entre PIB e consumo de diferentes tipos de energia fóssil.

    Parameters
    ----------
    df : DataFrame
        DataFrame com os dados de energia e PIB, agrupados por país.

    Returns
    -------
    None.
        O gráfico de barras é salvo como um arquivo PNG no diretório '../plots/'.
    """
    
    # Dicionário para armazenar as contagens de correlação
    correlation_counts = {
        'Energy Type': [],
        'Alta Correlação': [],
        'Correlação Moderada': [],
        'Baixa Correlação': []
    }

    # Calcular as contagens para cada tipo de energia
    for energy, col in zip(['Carvão', 'Gás', 'Petróleo'], 
                            ['coal_cons_per_capita', 'gas_energy_per_capita', 'oil_energy_per_capita']):
        counts = {'high': 0, 'moderate': 0, 'low': 0}

        # Agrupar por país
        for country, group in df.groupby('country'):
            group_clean = group.dropna(subset=['gdp', col])
            if len(group_clean) > 1:
                corr_matrix = group_clean[['gdp', col]].corr()
                correlation_value = corr_matrix.iloc[0, 1]

                # Classificar a correlação
                if abs(correlation_value) > 0.7:
                    counts['high'] += 1
                elif abs(correlation_value) > 0.3:
                    counts['moderate'] += 1
                else:
                    counts['low'] += 1

        # Adiciona os resultados ao dicionário de contagens
        correlation_counts['Energy Type'].append(energy)
        correlation_counts['Alta Correlação'].append(counts['high'])
        correlation_counts['Correlação Moderada'].append(counts['moderate'])
        correlation_counts['Baixa Correlação'].append(counts['low'])

    # DataFrame das contagens
    correlation_counts_df = pd.DataFrame(correlation_counts)

    cores = ['#0077B6', '#BCC1CE', '#BCC1CE']

    ax = correlation_counts_df.set_index('Energy Type').plot(kind='bar', figsize=(10, 6), color=cores)
    
    plt.title('Contagem de Países por Correlação entre\nPIB e Consumo de Energia Fóssil', fontsize=16, pad=14)
    plt.xlabel('Tipo de Energia', fontsize=12, labelpad=14)
    plt.ylabel('Número de Países', fontsize=12, labelpad=14)
    plt.xticks(rotation=0, fontsize=12)
    
    plt.legend(title=None, loc='upper right', fontsize=12, frameon=False)
    sns.despine()
    
    # Adicionar os valores no topo apenas das barras de alta correlação
    for container in ax.containers:
        if container.datavalues[0] == correlation_counts_df['Alta Correlação'][0]:
            ax.bar_label(container, label_type='edge', color= '#33415C', fontsize=12, padding=3)
            

    plt.savefig('../plots/plots_hipotese_4/correlations_counts.png', dpi=300, format='png')
    plt.show()
    plt.close()


energy_gdp_correlation(df)




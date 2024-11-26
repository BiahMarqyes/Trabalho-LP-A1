"""
Esse módulo contém funções que plotam os gráficos da hipótese 3.
A primeira função plota um gráfico de barras, 
a segunda e a terceira plotam um gráfico de linhas.
"""
import data_cleaner
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = pd.DataFrame(data_cleaner.demand_and_production)

# Agrupando por países
df_grouped = df.groupby('year').sum().reset_index()


# Plota o gráfico de barras empilhadas que compara a demanda e a produção por ano
def plot_comparison_demand_production(df_grouped):
    """
    Plota e estiliza o gráfico de barras empilhadas que compara a demanda de energia global 
    e a produção de energia renovável global por ano

    Args:
        df_grouped (DataFrame): dataset agrupado por ano
    """
    # Colunas que serão usadas para fazer o gráfico
    df_demand_production = pd.melt(
        df_grouped, id_vars='year', 
        value_vars=['electricity_demand', 'renewables_electricity'], 
        var_name='Tipo', value_name='Valor'
        )

    # Transformação dos dados para gráfico empilhado
    df_pivot = df_demand_production.pivot(index='year', columns='Tipo', values='Valor').fillna(0)

    # Tamanho do gráfico
    plt.figure(figsize=(11, 7))    

    # Criar o gráfico de barras empilhadas
    plt.bar(
        df_pivot.index, df_pivot['renewables_electricity'], 
        label='Produção de Energia Renovável', color=(8/255, 27/255, 70/255)
        )
    
    plt.bar(
        df_pivot.index, df_pivot['electricity_demand'], 
        bottom=df_pivot['renewables_electricity'], label='Demanda de Energia', 
        color=(49/255, 135/255, 196/255)
        )

    # Intervalos do eixo X
    intervalos_x = list(range(2000, 2022, 3))
    plt.xticks(intervalos_x, [str(x) for x in intervalos_x])

    # Estilizando o gráfico
    plt.title(
        'Comparação entre Demanda de Energia e\nProdução de Energia Renovável por Ano', 
        fontsize=17, pad=14
        )
    plt.xlabel('Ano', fontsize=12)
    plt.ylabel('Quant.\nde\nEnergia\nem TWh', rotation=0, labelpad=30, ha='center')
    plt.legend(loc='upper left', borderaxespad=3, fontsize=11.5)
    # Remover o contorno do gráfico
    sns.despine()
    
    #plt.show()

    # Salvar gráfico
    plt.savefig('../plots/plots_hipotese_3/grafico_1.png', format = 'png')


plot_comparison_demand_production(df_grouped)


# Plota o gráfico de linhas que compara a taxa de variação anual da demanda 
# e a taxa de variação anual da produção
def plot_variation_demand_production(df_grouped):
    """
    Plota e estiliza o gráfico de linhas que compara a proporcão da produção 
    de energia renovável com a demanda de energia global

    Args:
        df_grouped (DataFrame): dataset agrupado por ano
    """
    # Calcular a taxa de variação da demanda por ano usando o método pct_change()
    df_grouped['variation_demand'] = df_grouped['electricity_demand'].pct_change() * 100

    # Calcular a taxa de variação da produção por ano usando o método pct_change()
    df_grouped['variation_production'] = df_grouped['renewables_electricity'].pct_change() * 100
    
    # Criar o gráfico de linhas 
    plt.figure(figsize=(10,7))
    sns.lineplot(
        x='year', y='variation_demand', data=df_grouped, 
        label='Taxa de Variação - Demanda', marker='o', 
        color=(49/255, 135/255, 196/255)
        )
    sns.lineplot(
        x='year', y='variation_production', data=df_grouped, 
        label='Taxa de Variação - Produção', marker='o', 
        color=(8/255, 27/255, 70/255)
        )

    # Intervalos do eixo X
    intervalos_x = list(range(2000, 2022, 3))
    plt.xticks(intervalos_x, [str(x) for x in intervalos_x])

    # Estilizando o gráfico
    plt.title(
        'Comparação entre Taxa de Variação da Demanda e\nTaxa de Variação de Energia Renovável', 
        fontsize=17, pad=20
        )
    plt.xlabel('Ano', fontsize=12)
    plt.ylabel('Taxa\nde\nVariação (%)', rotation=0, labelpad=27, ha='center')
    plt.legend(fontsize=11)
    # Remover o contorno e as grades do gráfico
    sns.despine()
    
    # Salvar gráfico
    plt.savefig('../plots/plots_hipotese_3/grafico_2.png', format='png')


plot_variation_demand_production(df_grouped)  


# Plota o gráfico de linhas que compara a proporcão renovável/demanda por ano
def plot_ratio_production_demand(df_grouped):
    """
    Plota e estiliza o gráfico de linhas que compara a taxa de variação anual da demanda 
    de energia global e a taxa de variação anual da produção de energia renovável global

    Args:
        df_grouped (DataFrame): dataset agrupado por ano
    """
    # Cálculo da proporção renovável/demanda
    df_grouped['renewables_ratio'] = df_grouped['renewables_electricity'] / df_grouped['electricity_demand']

    # Tamanho do gráfico
    plt.figure(figsize=(10.5, 5)) 

    # Plotar gráfico
    plt.plot(
        df_grouped['year'], df_grouped['renewables_ratio'], 
        label='Proporção', color='#DC7200'
        )

    # Intervalos do eixo X
    intervalos_x = list(range(2000, 2022, 3))
    plt.xticks(intervalos_x, [str(x) for x in intervalos_x])

    # Intervalos do eixo Y
    intervalos_y = np.linspace(0, 0.5, 6)
    plt.yticks(intervalos_y, [f"{y * 100:.0f}%" for y in intervalos_y])

    # Personalizar o gráfico
    plt.title(
        'Proporção entre Produção de Energia Renovável\ne Demanda de Energia por Ano', 
        fontsize=17, pad=0)
    plt.xlabel('Ano', fontsize=12)
    plt.ylabel('Proporção\nRenováveis\nDemanda', rotation=0, labelpad=35, ha='center')
    # Remover o contorno do gráfico
    sns.despine()
    
    # Salvar gráfico
    plt.savefig('../plots/plots_hipotese_3/grafico_3.png', format = 'png')


plot_ratio_production_demand(df_grouped)


# Plota os gráficos de linhas que comparam a taxa de variação anual da demanda 
# e a taxa de variação anual da produção de cada um dos três países mais ricos 
def plot_variation_in_the_richest_countries(df):
    """
    Faz a média do pib anual de cada país;
    Encontra as três maiores médias;
    Plota e estiliza três gráficos de linhas que compara a taxa de variação anual da demanda 
    de energia global e a taxa de variação anual da produção de energia renovável global de cada 
    um dos três países mais ricos de acordo com a média do pib

    Args:
        df (DataFrame): dataset que vem da função demand_and_production em data_cleaner.py
    """
    # Os países mais ricos serão aqueles com maior média do pib
    gdp_mean = df.groupby('country')['gdp'].mean()

    # Tamanho 
    fig, axes = plt.subplots(1, 3, figsize=(16, 6))

    # Intervalos do eixo Y
    intervalos_y = list(range(-20, 50, 10))
    
    # Pega os três países mais ricos e suas informações e gera seus gráficos
    for i in range(3):
        rich = gdp_mean.idxmax()
        print(rich)
        df_rich = df[df['country'] == rich].copy()
        # Calcular a taxa de variação da demanda por ano usando o método pct_change()
        df_rich['variation_demand'] = df_rich['electricity_demand'].pct_change() * 100
        # # Calcular a taxa de variação da produção por ano usando o método pct_change()
        df_rich['variation_production'] = df_rich['renewables_electricity'].pct_change() * 100

        sns.lineplot(
            x='year', y='variation_demand', data=df_rich, label='Taxa de Variação - Demanda', 
            marker='o', ax=axes[i], legend=False, color=(49/255, 135/255, 196/255)
            )
        sns.lineplot(
            x='year', y='variation_production', data=df_rich, label='Taxa de Variação - Produção', 
            marker='o', ax=axes[i], legend=False, color=(8/255, 27/255, 70/255)
            )
        axes[i].set_title(f"{rich}", fontsize=16, y=0.9)
        axes[i].set_xlabel('Ano', fontsize=12, labelpad=6)
        axes[i].tick_params()

        # Aplicar os mesmos intervalos de y para cada subplot
        axes[i].set_yticks(intervalos_y)
        axes[i].set_ylim(-25, 47.5)
    
        # Elimina o país i mais rico da série
        gdp_mean = gdp_mean.drop(rich)

    # Estilizando o gráfico
    fig.suptitle(
        'Comparação entre Taxa de Variação da Demanda e Taxa de Variação de Energia Renovável dos 3 países mais ricos',
        fontsize=19
        )
    fig.subplots_adjust(top=0.81)
    
    axes[0].set_ylabel(
        'Taxa de\nVariação\n(%)', rotation=0, labelpad=35, 
        ha='center', fontsize=11.5
        )
    axes[1].set_ylabel('')
    axes[2].set_ylabel('')
    
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles, labels, loc='upper center', bbox_to_anchor=(0.5, 0.92), 
        ncol=2, fontsize=14
        )

    # Remover o contorno e as grades do gráfico
    sns.despine()

    # Salvar gráfico
    plt.savefig('../plots/plots_hipotese_3/grafico_4.png', format='png')
     

plot_variation_in_the_richest_countries(df)


# Plota o gráfico de linhas que compara a proporcão renovável/demanda por ano 
# dos 3 países mais ricos 
def plot_top_3_ratio_production_demand(df):
    """
    Faz a média do pib anual de cada país;
    Encontra as três maiores médias;
    Plota e estiliza um gráfico de linhas que compara a proporcão da produção de 
    energia renovável com a demanda de energia global dos três países mais 
    ricos de acordo com a média do pib

    Args:
        df (DataFrame): dataset que vem da função demand_and_production em data_cleaner.py
    """
    # Os países mais ricos serão aqueles com maior média do pib
    gdp_mean = df.groupby('country')['gdp'].mean()

    # Tamanho do gráfico
    plt.figure(figsize=(10.5, 5)) 

    # Cores das linhas 
    colors = ['#003089', '#CB1212', '#068127']

    # Pega os três países mais ricos e suas informações e gera seus gráficos
    for i in range(3):
        rich = gdp_mean.idxmax()
        print(rich)
        df_rich = df[df['country'] == rich].copy()

        # Cálculo da proporção renovável/demanda
        df_rich['renewables_ratio'] = df_rich['renewables_electricity'] / df_rich['electricity_demand']

        # Plota 
        sns.lineplot(
            x=df_rich['year'], y=df_rich['renewables_ratio'], 
            label=f"{rich}", color=colors[i]
            )
    
        # Elimina o país i mais rico da série
        gdp_mean = gdp_mean.drop(rich)

    # Intervalos do eixo X
    intervalos_x = list(range(2000, 2022, 3))
    plt.xticks(intervalos_x, [str(x) for x in intervalos_x])

    # Intervalos do eixo Y
    intervalos_y = np.linspace(0, 0.5, 6)
    plt.yticks(intervalos_y, [f"{y * 100:.0f}%" for y in intervalos_y])

    # Personalizar o gráfico
    plt.title(
        'Proporção entre Produção de Energia Renovável\ne Demanda de Energia por Ano', 
        fontsize=17, pad=0)
    plt.xlabel('Ano', fontsize=12)
    plt.ylabel('Proporção\nRenováveis\nDemanda', rotation=0, labelpad=35, ha='center')
    plt.legend(borderaxespad=3)
    # Remover o contorno do gráfico
    sns.despine()
    
    # Salvar gráfico
    plt.savefig('../plots/plots_hipotese_3/grafico_5.png', format = 'png')


plot_top_3_ratio_production_demand(df)


# Cálculos para verificar correlações 
# Cálculo da correlação entre as duas variáveis (geração e produção global)  
correlation = np.corrcoef(df_grouped['electricity_demand'], df_grouped['renewables_electricity'])[0, 1]  
print(correlation)

from data_cleaner import demand_and_production
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("data/World Energy Consumption.csv")
df2 = demand_and_production(df)

# Agrupando por países
df_grouped = df2.groupby('year').sum().reset_index()


# Plota o gráfico de barras empilhadas que compara a demanda e a produção por ano
def plot_comparison_demand_production(df_grouped):
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
        label='Produção de Energia Renovável', color=(20/255, 117/255, 112/255)
        )
    
    plt.bar(
        df_pivot.index, df_pivot['electricity_demand'], 
        bottom=df_pivot['renewables_electricity'], label='Demanda de Energia', 
        color=(151/255, 201/255, 181/255)
        )

    # Intervalos do eixo X
    intervalos_x = list(range(2000, 2022, 3))
    plt.xticks(intervalos_x, [str(x) for x in intervalos_x])

    # Estilizando o gráfico
    plt.title('Comparação entre Demanda de Energia e\nProdução de Energia Renovável por Ano', fontsize=17, pad=15)
    plt.xlabel('Ano', fontsize=12)
    plt.ylabel('Quant.\nde\nEnergia\nem TWh', rotation=0, labelpad=30, ha='center')
    plt.legend(loc='upper left', borderaxespad=4)
    # Remover o contorno do gráfico
    sns.despine()
    
    #plt.show()

    # Salvar gráfico
    plt.savefig('plots/grafico1.png', format = 'png')


plot_comparison_demand_production(df_grouped)





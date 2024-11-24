"""
Módulo responsável por gerar gráficos sobre a relação entre consumo de energia, população, demanda e importações de eletricidade
"""

import numpy as np
import data_cleaner
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

df_main_1 = pd.DataFrame(data_cleaner.consumption_population)

def plot_consumption_population(df_main_1):
    # Criando um df_annual_consumption com os dados totais de população por ano
    df_annual_consumption = pd.DataFrame()
    
    df_annual_consumption["year"] = df_main_1["year"]
    df_annual_consumption["primary_energy_consumption"] = df_main_1["primary_energy_consumption"]
    
    df_consumption = df_main_1.groupby("year")["primary_energy_consumption"].sum().reset_index()
    
    # Criando um df_annual_population com os dados totais de população por ano
    df_annual_population = pd.DataFrame()
    
    df_annual_population["year"] = df_main_1["year"]
    df_annual_population["population"] = df_main_1["population"]
    
    df_population = df_main_1.groupby("year")["population"].sum().reset_index()

    # Criando um df_annual_consumption_and_population com os dados totais de população por ano e de consumo por ano
    df_annual_consumption_and_population = pd.DataFrame()
    
    df_annual_consumption_and_population["year"] = df_consumption["year"]
    df_annual_consumption_and_population["primary_energy_consumption"] = df_consumption["primary_energy_consumption"]
    df_annual_consumption_and_population["population"] = df_population["population"]

    # Gráfico de linhas para o consumo de energia e população
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    ax1.plot(df_annual_consumption_and_population["year"], df_annual_consumption_and_population["primary_energy_consumption"], label="Consumo de energia", color="blue")
    ax1.set_title("Consumo de energia ao Longo dos Anos")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Values")
    ax1.legend()

    ax2.plot(df_annual_consumption_and_population["year"], df_annual_consumption_and_population["population"], label="População", color="purple")
    ax2.set_title("População ao Longo dos Anos")
    ax2.set_xlabel("Year")
    ax2.set_ylabel("Values")
    ax2.legend()
    
    # Gráfico de dispersão para o consumo de energia e população
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=df_annual_consumption_and_population["primary_energy_consumption"], y=df_annual_consumption_and_population["population"], color='blue', label='Consumo de Energia x População')

    # Adicionando uma reta de regressão
    coef = np.polyfit(df_annual_consumption_and_population["primary_energy_consumption"], df_annual_consumption_and_population["population"], 1)  # Regressão linear (reta)
    poly1d_fn = np.poly1d(coef)  # Equação da reta

    plt.plot(df_annual_consumption_and_population["primary_energy_consumption"], poly1d_fn(df_annual_consumption_and_population["primary_energy_consumption"]), color='red', label='Reta de Regressão')

    plt.title('Relação entre Consumo de Energia e População')
    plt.xlabel('Consumo de Energia')
    plt.ylabel('População')
    plt.legend()
    plt.grid()

    # Mostrar o gráfico
    plt.show()
    
    return fig

plot_consumption_population(df_main_1)

df_main_2 = pd.DataFrame(data_cleaner.balance_import)

def plot_electricity_balance_import(df_main_2):
    # Criando um df_annual_electricity_balance com os dados totais do balanço de energia por ano
    df_annual_electricity_balance = pd.DataFrame()
    
    df_annual_electricity_balance["year"] = df_main_2["year"]
    df_annual_electricity_balance["electricity_balance"] = df_main_2["electricity_balance"]
    
    df_electricity_balance = df_main_2.groupby("year")["electricity_balance"].sum().reset_index()
    
    # Criando um df_annual_imports com os dados totais de importação por ano
    df_annual_imports = pd.DataFrame()
    
    df_annual_imports["year"] = df_main_2["year"]
    df_annual_imports["net_elec_imports"] = df_main_2["net_elec_imports"]
    
    df_imports = df_main_2.groupby("year")["net_elec_imports"].sum().reset_index()

    # Criando um df_annual_electricity_balance_and_import com os dados totais de importação por ano e de balanço de eletricidade por ano
    df_annual_electricity_balance_and_import = pd.DataFrame()
    
    df_annual_electricity_balance_and_import["year"] = df_electricity_balance["year"]
    df_annual_electricity_balance_and_import["electricity_balance"] = df_electricity_balance["electricity_balance"]
    df_annual_electricity_balance_and_import["net_elec_imports"] = df_imports["net_elec_imports"]
    
    # Gráfico de linhas para o balanço de energia elétrica e importação
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    
    ax1.plot(df_annual_electricity_balance_and_import["year"], df_annual_electricity_balance_and_import["electricity_balance"], label="Balanço de energia", color="blue")
    ax1.set_title("Balanço de energia elétrica ao Longo dos Anos")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Values")
    ax1.legend()
    
    ax2.plot(df_annual_electricity_balance_and_import["year"], df_annual_electricity_balance_and_import["net_elec_imports"], label="Importações", color="purple")
    ax2.set_title("Importação ao Longo dos Anos")
    ax2.set_xlabel("Year")
    ax2.set_ylabel("Values")
    ax2.legend()
    
    # Gráfico de dispersão para o balanço de energia elétrica e importação
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=df_annual_electricity_balance_and_import["electricity_balance"], y=df_annual_electricity_balance_and_import["net_elec_imports"], color='blue', label='Dados')
    
    # Adicionando uma reta de regressão
    coef = np.polyfit(df_annual_electricity_balance_and_import["electricity_balance"], df_annual_electricity_balance_and_import["net_elec_imports"], 1)  # Regressão linear (reta)
    poly1d_fn = np.poly1d(coef)  # Equação da reta
    
    plt.plot(df_annual_electricity_balance_and_import["electricity_balance"], poly1d_fn(df_annual_electricity_balance_and_import["electricity_balance"]), color='red', label='Reta de Regressão')
    
    plt.title('Relação entre Balanço de Energia e Importação')
    plt.xlabel('Balanço de Energia')
    plt.ylabel('Importação')
    plt.legend()
    plt.grid()
    
    plt.show()
    
    return plt

plot_electricity_balance_import(df_main_2)

df_main_3 = pd.DataFrame(data_cleaner.demand_import)

def plot_electricity_demand_import(df_main_3):
    # Criando um df_annual_electricity_demand com os dados totais da demanda de eletricidade por ano.
    df_electricity_demand = pd.DataFrame()
    
    df_electricity_demand["year"] = df_main_3["year"]
    df_electricity_demand["electricity_demand"] = df_main_3["electricity_demand"]
    
    df_annual_electricity_demand = df_main_3.groupby("year")["electricity_demand"].sum().reset_index()
    
    # Criando um df_annual_imports com os dados totais de importação por ano.
    df_imports = pd.DataFrame()
    
    df_imports["year"] = df_main_3["year"]
    df_imports["net_elec_imports"] = df_main_3["net_elec_imports"]
    
    df_annual_imports = df_main_3.groupby("year")["net_elec_imports"].sum().reset_index()

    # Criando um df_annual_electricity_demand_and_import com os dados totais de importação por ano e de demanda de eletricidade por ano.
    df_annual_electricity_demand_and_import = pd.DataFrame()
    
    df_annual_electricity_demand_and_import["year"] = df_annual_electricity_demand["year"]
    df_annual_electricity_demand_and_import["electricity_demand"] = df_annual_electricity_demand["electricity_demand"]
    df_annual_electricity_demand_and_import["net_elec_imports"] = df_annual_imports["net_elec_imports"]
    
    # Gráfico de linhas para a demanda de eletricidade e importação
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    
    ax1.plot(df_annual_electricity_demand_and_import["year"], df_annual_electricity_demand_and_import["electricity_demand"], label="Demanda de eletricidade", color="blue")
    ax1.set_title("Demanda de eletricidade ao Longo dos Anos")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Values")
    ax1.legend()
    
    ax2.plot(df_annual_electricity_demand_and_import["year"], df_annual_electricity_demand_and_import["net_elec_imports"], label="Importações", color="purple")
    ax2.set_title("Importação ao Longo dos Anos")
    ax2.set_xlabel("Year")
    ax2.set_ylabel("Values")
    ax2.legend()
    
    # Gráfico de dispersão para a demanda de eletricidade e importação
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=df_annual_electricity_demand_and_import["electricity_demand"], y=df_annual_electricity_demand_and_import["net_elec_imports"], color='blue', label='Dados')
    
    # Adicionando uma reta de regressão
    coef = np.polyfit(df_annual_electricity_demand_and_import["electricity_demand"], df_annual_electricity_demand_and_import["net_elec_imports"], 1)  # Regressão linear (reta)
    poly1d_fn = np.poly1d(coef)  # Equação da reta
    
    plt.plot(df_annual_electricity_demand_and_import["electricity_demand"], poly1d_fn(df_annual_electricity_demand_and_import["electricity_demand"]), color='red', label='Reta de Regressão')
    
    plt.title('Relação entre Demanda de eletricidade e Importação')
    plt.xlabel('Demanda de eletricidade')
    plt.ylabel('Importação')
    plt.legend()
    plt.grid()
    
    plt.show()
    
    return plt

plot_electricity_demand_import(df_main_3)

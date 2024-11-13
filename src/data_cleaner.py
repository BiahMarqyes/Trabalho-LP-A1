"""
Esse módulo contém funções que limpam o dataset e o preparam para cada uma das hipóteses.
"""
import pandas as pd

df = pd.read_csv("data/World Energy Consumption.csv")

columns = df.columns


# LIMPEZA DE DADOS PARA A HIPÓTESE 1


# LIMPEZA DE DADOS PARA A HIPÓTESE 2


# LIMPEZA DE DADOS PARA A HIPÓTESE 3
def demand_and_production(df):
    """
    Elimina entradas na coluna 'country' que não são países usando uma lista de exclusão pré-definida;
    Seleciona as colunas necessárias para a análise, ou seja, país, ano, pib, demanda e produção;
    Exclui linhas que contêm valores nulos nas colunas de demanda ou produção;
    Filtra os dados para o período de 2000 a 2021, que é onde a maioria dos países têm dados completos.

    Args:
        df (DataFrame): dataset base do trabalho

    Returns:
        df_clean (DataFrame): contém apénas os dados necessários para a análise
    """    
    # A coluna country contém países, continentes e blocos econômicos, como só queremos analisar os países vamos eliminar os que não são
    # Criamos uma lista com todos os nomes que aparecem na coluna country
    unique_countries = df['country'].unique().tolist() 
    print(unique_countries)
    # Usando o chatgpt para avaliar quais nomes não são de países, geramos a lista non_countries
    non_countries = [
    'ASEAN (Ember)', 'Africa', 'Africa (EI)', 'Africa (Ember)', 'Africa (Shift)', 
    'Asia', 'Asia & Oceania (EIA)', 'Asia (Ember)', 'Asia Pacific (EI)', 
    'Asia and Oceania (Shift)', 'Australia and New Zealand (EIA)', 'CIS (EI)', 
    'Central & South America (EIA)', 'Central America (EI)', 'Central and South America (Shift)', 
    'Democratic Republic of Congo', 'EU28 (Shift)', 'East Germany (EIA)', 'Eastern Africa (EI)', 
    'Eurasia (EIA)', 'Eurasia (Shift)', 'Europe', 'Europe (EI)', 'Europe (Ember)', 
    'Europe (Shift)', 'European Union (27)', 'European Union (EIA)', 'Falkland Islands', 
    'G20 (Ember)', 'G7 (Ember)', 'Hawaiian Trade Zone (EIA)', 'High-income countries', 
    'IEO - Africa (EIA)', 'IEO - Middle East (EIA)', 'IEO OECD - Europe (EIA)', 
    'Latin America and Caribbean (Ember)', 'Low-income countries', 'Lower-middle-income countries', 
    'Mexico, Chile, and other OECD Americas (EIA)', 'Middle Africa (EI)', 'Middle East (EI)', 
    'Middle East (EIA)', 'Middle East (Ember)', 'Middle East (Shift)', 'Non-OECD (EI)', 
    'Non-OECD (EIA)', 'Non-OPEC (EI)', 'Non-OPEC (EIA)', 'North America', 'North America (EI)', 
    'North America (Ember)', 'North America (Shift)', 'OECD (EI)', 'OECD (EIA)', 'OECD (Ember)', 
    'OECD (Shift)', 'OECD - Asia And Oceania (EIA)', 'OECD - Europe (EIA)', 'OECD - North America (EIA)', 
    'OPEC (EI)', 'OPEC (EIA)', 'OPEC (Shift)', 'OPEC - Africa (EIA)', 'OPEC - South America (EIA)', 
    'Oceania', 'Oceania (Ember)', 'Other Non-OECD - America (EIA)', 'Other Non-OECD - Asia (EIA)', 
    'Other Non-OECD - Europe and Eurasia (EIA)', 'Persian Gulf (EIA)', 'Persian Gulf (Shift)', 
    'South and Central America (EI)', 'South America', 'South Korea and other OECD Asia (EIA)', 
    'U.S. Pacific Islands (EIA)', 'U.S. Territories (EIA)', 'USSR', 'United States Pacific Islands (Shift)', 
    'United States Territories (Shift)', 'Upper-middle-income countries', 'Wake Island (EIA)', 
    'Wake Island (Shift)', 'West Germany (EIA)', 'Western Africa (EI)', 'World', 'Yugoslavia'
     ]
    # Agora tiramso todas as linhas do df que comtém qualquer um desses não países
    df = df[~df['country'].isin(non_countries)]
    
    # Colunas necessárias para a análise 
    df_columns_needed = df[['country','year','gdp','electricity_demand','renewables_electricity']]
    
    # Eliminação das linhas que não contenham a demanda ou a produção
    no_nulls_rows = df_columns_needed.dropna(subset=['electricity_demand','renewables_electricity'], how='any')
    
    # Praticamente todos países contém dados entre 2000 e 2021, então a análise será feita nesse período 
    df_clean = no_nulls_rows[(no_nulls_rows['year'] >= 2000) & (no_nulls_rows['year'] <= 2021)]
    
    return df_clean


# LIMPEZA DE DADOS PARA A HIPÓTESE 4

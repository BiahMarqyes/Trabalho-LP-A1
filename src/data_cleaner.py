"""
Esse módulo contém funções que limpam o dataset e o preparam para cada uma das hipóteses.
"""
import pandas as pd
import numpy as np

df = pd.read_csv("./data/World Energy Consumption.csv")

columns = df.columns

# LIMPEZA DE DADOS PARA A HIPÓTESE 1


# LIMPEZA DE DADOS PARA A HIPÓTESE 2

# Dicionário com os países de cada continente (feito com ChatGPT)
countries_by_continent_map = {
    "Antarctica": ["Antarctica"],
    "Africa": ["Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cameroon", "Cape Verde",
        "Central African Republic", "Chad", "Comoros", "Congo", "Cote d'Ivoire", "Democratic Republic of Congo", 
        "Djibouti", "Egypt", "Equatorial Guinea", "Eritrea", "Eswatini", "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea", 
        "Guinea-Bissau", "Kenya", "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius", 
        "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", "Sao Tome and Principe", "Senegal", "Seychelles", 
        "Sierra Leone", "Somalia", "South Africa", "South Sudan", "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe"],
    "Asia": ["Afghanistan", "Armenia", "Azerbaijan", "Bahrain", "Bangladesh", "Bhutan", "Brunei", "Cambodia", "China", "Cyprus",
        "Georgia", "India", "Indonesia", "Iran", "Iraq", "Israel", "Japan", "Jordan", "Kazakhstan", "Kuwait", "Kyrgyzstan", "Laos", "Lebanon",
        "Malaysia", "Maldives", "Mongolia", "Myanmar", "Nepal", "North Korea", "Oman", "Pakistan", "Palestine", "Philippines", "Qatar",
        "Saudi Arabia", "Singapore", "South Korea", "Sri Lanka", "Syria", "Taiwan", "Tajikistan", "Thailand", "Timor-Leste", "Turkey", 
        "Turkmenistan", "United Arab Emirates", "Uzbekistan", "Vietnam", "Yemen"],
    "Europe": ["Albania", "Andorra", "Armenia", "Austria", "Azerbaijan", "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia", "Cyprus",
        "Czechia", "Denmark", "Estonia", "Finland", "France", "Georgia", "Germany", "Greece", "Hungary", "Iceland", "Ireland", "Italy", "Kosovo", "Latvia",
        "Lithuania", "Luxembourg", "Malta", "Moldova", "Monaco", "Montenegro", "Netherlands", "North Macedonia", "Norway", "Poland", "Portugal", "Romania", 
        "Russia", "San Marino", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "Ukraine", "United Kingdom"],
    "North America": ["Canada", "Greenland", "Mexico", "United States"],
    "Central America": ["Antigua and Barbuda", "Bahamas", "Barbados", "Belize", "Costa Rica", "Cuba", "Dominica", "Dominican Republic", "El Salvador", "Grenada", 
        "Guatemala", "Haiti", "Honduras", "Jamaica", "Nicaragua", "Panama", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Trinidad and Tobago"],
    "South America": ["Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador", "Guyana", "Paraguay", "Peru", "Suriname", "Uruguay", "Venezuela"],
    "Oceania": ["Australia", "Fiji", "Kiribati", "Marshall Islands", "Micronesia", "Nauru", "New Zealand", "Palau", 
        "Papua New Guinea", "Samoa", "Solomon Islands", "Tonga", "Tuvalu", "Vanuatu"]
}

def continent_identifier(country: str) -> str:
    """
    Identifica o continente de um país.

    Parameters
    ----------
    country : str
        Nome do país.

    Returns
    -------
    str
        Nome do continente ao qual o país pertence.
    """
    for continent, countries in countries_by_continent_map.items():
        if country in countries:
            return continent
    return None

def renewable_energy_consumption_by_continent(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpa o DataFrame original para conter apenas dados de consumo de energia renovável e população válidos,
    adicionando uma coluna de continentes para agrupar os dados dos países.

    Parameters
    ----------
    df: pd.DataFrame
        O DataFrame original.

    Returns
    -------
    pd.DataFrame
        O novo DataFrame com os continentes e dados agrupados.
    """
    cols_numericas = ["year", "population", "biofuel_consumption", "hydro_consumption",
        "other_renewable_consumption", "renewables_consumption", "solar_consumption", "wind_consumption"]

    # Confirma que as colunas são numéricas
    df[cols_numericas] = df[cols_numericas].apply(pd.to_numeric, errors="coerce")

    # Cria uma nova coluna no DataFrame com o continente de cada país
    df["continent"] = df["country"].apply(continent_identifier)

    # Filtra as colunas de interesse
    df_continents = df[["continent", "year", "population", "biofuel_consumption", "hydro_consumption", 
        "other_renewable_consumption", "renewables_consumption", "solar_consumption", "wind_consumption"]]

    # Filtra as linhas que não possuem dados em nenhuma dessas colunas
    filtered_df = df_continents.dropna(subset=["biofuel_consumption", "hydro_consumption", "other_renewable_consumption", 
        "renewables_consumption", "solar_consumption", "wind_consumption"], how='all').copy()
    
    # Trocam os valores nulos por 0
    filtered_df['biofuel_consumption'].fillna(0)
    filtered_df['hydro_consumption'].fillna(0)
    filtered_df['other_renewable_consumption'].fillna(0)
    filtered_df['renewables_consumption'].fillna(0)
    filtered_df['solar_consumption'].fillna(0)
    filtered_df['wind_consumption'].fillna(0)

    # Retira população nula
    filtered_df = filtered_df[filtered_df["population"].notna()]

    # Coloca o intervalo de tempo desejado
    new_df = filtered_df[filtered_df["year"].between(2000, 2022)]

    return new_df

renewable_energy_consumption_continental = renewable_energy_consumption_by_continent(df)

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
    # Agora tiramos todas as linhas do df que comtém qualquer um desses não países
    df = df[~df['country'].isin(non_countries)]
    
    # Colunas necessárias para a análise 
    df_columns_needed = df[['country','year','gdp','electricity_demand','renewables_electricity']]
    
    # Eliminação das linhas que não contenham a demanda ou a produção
    no_nulls_rows = df_columns_needed.dropna(subset=['electricity_demand','renewables_electricity'], how='any')
    
    # Praticamente todos países contém dados entre 2000 e 2021, então a análise será feita nesse período 
    df_clean = no_nulls_rows[(no_nulls_rows['year'] >= 2000) & (no_nulls_rows['year'] <= 2021)]
    
    return df_clean


# LIMPEZA DE DADOS PARA A HIPÓTESE 4
def GDP_and_fossil_energy_consumption(df):
    """
    Gera um df agrupado por país com todas colunas necessárias para a análise 

    Parameters
    ----------
    df : DataFrame
    Returns
    -------
    new_df : DataFrame

    """
    # coal, fossil gas, oil, GDP, country
    df_fossil_energy = df[['country','year','gdp','coal_cons_per_capita','fossil_energy_per_capita','gas_energy_per_capita','oil_energy_per_capita']]
    
    # Remoção das linhas que não contem dados relativos à verificação
    no_nulls_rows = df_fossil_energy.dropna(subset=['coal_cons_per_capita','fossil_energy_per_capita','gas_energy_per_capita','oil_energy_per_capita'], how='all')
    
    # array de países ou conjuntos agrupados onde o PIB não consta em nenhum dos anos verificados
    null_gdp_countries = df.groupby('country').filter(lambda x: x['gdp'].isna().all())['country'].unique()
    
    # DataFrame sem ps países e agrupados cujo PIB não consta
    new_df = no_nulls_rows[~no_nulls_rows['country'].isin(null_gdp_countries)]
    
    return new_df



GDP_and_fossil_energy_frame = GDP_and_fossil_energy_consumption(df)

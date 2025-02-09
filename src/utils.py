from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math

# load the .env file variables
load_dotenv()


def db_connect():
    import os
    engine = create_engine(os.getenv('DATABASE_URL'))
    engine.connect()
    return engine
    

def columnas_categoricas(df, lista_num_cat=[]):
    columnas_categoricas = []
    for column in df.columns:
        if df[column].dtype == 'object':
            columnas_categoricas.append(column)
    if len(lista_num_cat)>0:
        columnas_categoricas.extend(lista_num_cat)
    return columnas_categoricas

def analisis_categorico_categorico(df,lista_num_cat=[]):
    col_cat = columnas_categoricas(df,lista_num_cat)
    largo = len(col_cat)
    parte_entera = largo//3
    resto = largo%3
    parte_entera+=1
    if resto == 0:
        parte_entera -=1
    
    fig, axis = plt.subplots(parte_entera,3,figsize=(10,7))

    for column in col_cat:
        fila=col_cat.index(column)//3
        columna = col_cat.index(column)%3
        if columna != 0:
            sns.histplot(ax= axis[fila,columna],data=df,x=column).set(ylabel=None,xticks=[])
        else:
            sns.histplot(ax= axis[fila,columna],data=df,x=column).set(xticks=[])

    plt.tight_layout()
    plt.show()

def columnas_numericas(df,columnas_excluidas=[]):
    columnas_numericas = []
    for column in df.columns:
        if df[column].dtype in ['int64','float64']:
            if column not in columnas_excluidas:
                columnas_numericas.append(column)  
    return columnas_numericas

def analisis_numerico_numerico(df,y,columnas_excluidas=[],limites=[]):
    col_num = columnas_numericas(df,columnas_excluidas)
    if df[y].dtype not in ['int64','float64']:
        col_num.remove(y)
    largo = len(col_num)
    parte_entera = (largo//2)*2
    resto = largo%4
    parte_entera +=2
    if resto == 0:
        parte_entera-=2
    num_de_gridspec = math.ceil(parte_entera/2)
    lista_hr = [5,1]*num_de_gridspec
    print(parte_entera)
    print(lista_hr)
    fig, axis = plt.subplots(parte_entera,2,figsize=(10,10),gridspec_kw={"height_ratios":lista_hr})

    for column in col_num:
        fila = (col_num.index(column)//2)*2
        columna = col_num.index(column)%2
        if len(limites)>0:
            if 0<= col_num.index(column)*2 < len(limites):
                if limites[col_num.index(column)*2] != None:
                    sns.histplot(ax=axis[fila,columna],data=df,x=column).set(xlim=(limites[col_num.index(column)*2],limites[col_num.index(column)*2+1]))
                    sns.boxplot(ax=axis[fila+1,columna],data=df,x=column).set(xlim=(limites[col_num.index(column)*2],limites[col_num.index(column)*2+1]))
                else:
                    sns.histplot(ax=axis[fila,columna],data=df,x=column)
                    sns.boxplot(ax=axis[fila+1,columna],data=df,x=column)
            else:
                sns.histplot(ax=axis[fila,columna],data=df,x=column)
                sns.boxplot(ax=axis[fila+1,columna],data=df,x=column)
        else:
            sns.histplot(ax=axis[fila,columna],data=df,x=column)
            sns.boxplot(ax=axis[fila+1,columna],data=df,x=column)
    plt.tight_layout()
    plt.show()
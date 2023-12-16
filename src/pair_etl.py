#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 

import os
import sys

#imputacion de nulos
from sklearn.impute import SimpleImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.impute import KNNImputer

from dotenv import load_dotenv
load_dotenv()
sys.path.append("../")
pd.set_option('display.max_columns', None) 

# %%

def lectura_archivos ():
   df_clientes = pd.read_csv('clientes.csv')
   df_productos = pd.read_csv('productos.csv', on_bad_lines='skip')
   df_ventas = pd.read_csv('ventas.csv')
   
   df_union_1 = df_clientes.merge(df_ventas, left_on='id', right_on= 'ID_Cliente', how= 'left')
   df_final = df_union_1.merge(df_productos, left_on= 'ID_Producto', right_on= 'ID', how='left' )

   return df_final
#%%  
df_final = lectura_archivos()
#%%
# generamos un DataFrame para los valores nulos
def datos_generales (dataframe):
    print("Los nulos que tenemos en el conjunto de datos son:")
    df_nulos = pd.DataFrame(dataframe.isnull().sum() / dataframe.shape[0] * 100, columns = ["%_nulos"])
    print(df_nulos[df_nulos["%_nulos"] > 0])
    
    print("\n ..................... \n")
    print(f"Los tipos de las columnas son:")
    print(pd.DataFrame(dataframe.dtypes, columns = ["tipo_dato"]))
    
    
    print("\n ..................... \n")
    print("Los valores que tenemos para las columnas categóricas son: ")
    dataframe_categoricas = dataframe.select_dtypes(include = "O")
    
    for col in dataframe_categoricas.columns:
        print(f"La columna {col.upper()} tiene las siguientes valore únicos:")
        print(pd.DataFrame(dataframe[col].value_counts()).head())    
#%%
resultados = datos_generales(df_final)
# %%
def homogeneizar_columnas(dataframe):
   columnas_minus = {columna: columna.lower() for columna in df_final.columns} 
   df_final.rename(columns = columnas_minus ,inplace = True)

   df_final.drop(columns=['id_cliente', 'descripción_2'],inplace=True)

   df_final.rename
   return df_final
# %%
homogeneizar_columnas(df_final)
#%%
#Empezamos a gestionar nulos
#Variables categoricas

#lista de columnas categóricas que tienen nulos
nulos_categoricas = df_final[df_final.columns[df_final.isnull().any()]].select_dtypes(include = "O").columns
print("Las columnas categóricas que tienen nulos son : \n ")
print(nulos_categoricas)
# %%
for columna in nulos_categoricas:
    print(f"La distribución de las categorías para la columna {columna.upper()}")
    display(df_final[columna].value_counts() / df_final.shape[0])
    print("..........")
# %%
df_final.columns
#%%
df_final['']
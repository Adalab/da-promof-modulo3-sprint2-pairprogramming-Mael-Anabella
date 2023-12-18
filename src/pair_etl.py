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
#%%
df_final.head(3)
# %%
def homogeneizar_columnas(dataframe):
   
   df_final.drop(columns=['id', 'Descripción_2'], inplace=True)
   columnas_minus = {columna: columna.lower() for columna in df_final.columns} 
   df_final.rename(columns = columnas_minus ,inplace = True)
   df_final.replace({'id_ventas':'id'})
   return df_final
# %%
homogeneizar_columnas(df_final)
#%%
#Empezamos a gestionar nulos
#Variables categoricas

def gestion_nulos (dataframe):
    #Nulos en el conjunto de datos
    print("Los nulos que tenemos en el conjunto de datos son:")
    df_nulos = pd.DataFrame(df_final.isnull().sum() / df_final.shape[0] * 100, columns = ["%_nulos"])
    print(df_nulos[df_nulos["%_nulos"] > 0])

    #lista de columnas categóricas que tienen nulos
    print(' ....... ')
    nulos_categoricas = df_final[df_final.columns[df_final.isnull().any()]].select_dtypes(include = "O").columns
    print("Las columnas categóricas que tienen nulos son : \n ")
    print(nulos_categoricas)

    for columna in nulos_categoricas:
        print(f"La distribución de las categorías para la columna {columna.upper()}")
        display(df_final[columna].value_counts() / df_final.shape[0])
        print("..........")
    #columnas numericas que tienen nulos
    nulos_numericas = df_final[df_final.columns[df_final.isnull().any()]].select_dtypes(include = np.number).columns
    print("Las columnas numéricas que tienen nulos son : \n ")
    print(nulos_numericas)
    #porcentajes de nulos por columna 
    df_final[nulos_numericas].isnull().sum() / df_final.shape[0]

#%%
#NULOS email             2.523364
#gender            8.504673
#city             12.897196
#country          16.168224
#address           3.831776
#id_cliente       90.654206
#id_producto      90.654206
#fecha_venta      90.654206
#cantidad         90.654206
#total            90.654206
#id               99.252336
#nombre_producto  99.252336
#categoría        99.252336
#precio           99.252336
#origen           99.252336
#descripción      99.252336
#%%
gestion_nulos(df_final)

# %%
df_final['email']=df_final['email'].replace(np.nan, "desconocido")
df_final['gender']=df_final['gender'].replace(np.nan, "desconocido")
df_final['country']=df_final['country'].replace(np.nan, "desconocido")
df_final['city']=df_final['city'].replace(np.nan, "desconocido")
df_final['id_cliente']=df_final['id_cliente'].replace(np.nan, "desconocido")
df_final['id_producto']=df_final['id_producto'].replace(np.nan, "desconocido")
df_final['fecha_venta']=df_final['fecha_venta'].replace(np.nan, "desconocido")
df_final['cantidad']=df_final['cantidad'].replace(np.nan, "desconocido")
df_final['total']=df_final['total'].replace(np.nan, "desconocido")
df_final['id']=df_final['id'].replace(np.nan, "desconocido")
df_final['nombre_producto']=df_final['nombre_producto'].replace(np.nan, "desconocido")
df_final['nombre_producto']=df_final['nombre_producto'].replace(np.nan, "desconocido")
df_final['categoría']=df_final['categoría'].replace(np.nan, "desconocido")
df_final['precio']=df_final['precio'].replace(np.nan, "desconocido")
df_final['origen']=df_final['origen'].replace(np.nan, "desconocido")
df_final['descripción']=df_final['descripción'].replace(np.nan, "desconocido")
# %%
df_final.info()

df_final.describe()
# %%
df_final['clientes'] = np.where(df_final['id_cliente'] == "desconocido", 'no dado de alta', 'dado de alta')

# %%
plt.figure(figsize=(8, 6))
sns.countplot(data=df_final, x='clientes')
plt.title('Clientes Dados de Alta vs No Dados de Alta')
plt.xlabel('Estado de Alta')
plt.ylabel('Cantidad de Clientes')
plt.show()
# %%

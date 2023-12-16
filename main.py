#%%
from src import pair_etl as pair 

# %%
df_final = pair.lectura_archivos()
#%%
datos_df = pair.datos_generales(df_final)
# %%
pair.homogeneizar_columnas(df_final)
#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


# In[2]:


url1 = r'C:\Users\ignacio.gutierrez\Cementos BSA\HBSA - Información Planificación Comercial\55. Data Analytics\1- Estrategia de Precios HPM\Servicios Complementarios\archivos_codigos\Bases BSA 21 y 22.xlsx'
url2 = r'C:\Users\ignacio.gutierrez\Cementos BSA\HBSA - Información Planificación Comercial\55. Data Analytics\1- Estrategia de Precios HPM\Servicios Complementarios\archivos_codigos\Bases polpaico 2021 y 2022.xlsx'
url3 = r'C:\Users\ignacio.gutierrez\Cementos BSA\HBSA - Información Planificación Comercial\55. Data Analytics\1- Estrategia de Precios HPM\Servicios Complementarios\archivos_codigos\Homologación y sus precios_v3.xlsx'
url4 = r'C:\Users\ignacio.gutierrez\Cementos BSA\HBSA - Información Planificación Comercial\55. Data Analytics\1- Estrategia de Precios HPM\Servicios Complementarios\archivos_codigos\base Polp 2023.xlsx'
url5 = r'C:\Users\ignacio.gutierrez\Cementos BSA\HBSA - Información Planificación Comercial\55. Data Analytics\1- Estrategia de Precios HPM\Servicios Complementarios\archivos_codigos\Base_BSA_2023.xlsx'

bsa_2021 = pd.read_excel(url1,sheet_name="BASE 2021 - SERVICIOS")
bsa_2022 = pd.read_excel(url1,sheet_name="BASE 2022 - SERVICIOS")
polp1y2 = pd.read_excel(url2,sheet_name="Bases polpaico 21 - 22, simplif")
polp2023 = pd.read_excel(url4,sheet_name="Base_limpia")
bsa_2023 = pd.read_excel(url5,sheet_name="Base_bsa_limpia")
homol = pd.read_excel(url3,sheet_name="Resumen Homologación")


# In[3]:


bsa_2023['Fecha factura'] = pd.to_datetime(bsa_2023['Fecha factura'])
bsa_2023['Periodo'] = bsa_2023['Fecha factura'].dt.strftime('%Y%m')
bsa_2023


# In[4]:


#Concatenamos las bases 
bsa_total = pd.concat([bsa_2021,bsa_2022,bsa_2023])


# In[5]:


#le cambiamos el tipo de datos a las columnas
homol["ID Servicio Polpaico"] = homol["ID Servicio Polpaico"].fillna("0").astype("int64")
homol["ID Servicio BSA"] = homol["ID Servicio BSA"].astype(str).apply(lambda x:x.strip())
bsa_total["Producto"] = bsa_total["Producto"].astype(str).apply(lambda x:x.strip())


# In[6]:


#Creamos los diccionarios para homologar los servicios y las familias
homologar_bsa_dict = dict(zip(homol["ID Servicio BSA"],homol["Homologación"]))
homologar_bsa_familia_dict = dict(zip(homol["Homologación"],homol["Grupo Servicio"]))
homologar_bsa_familia_dict[np.nan]=np.nan
homologar_bsa_familia_dict['nan']=np.nan
homologar_bsa_dict[np.nan]=np.nan
homologar_bsa_dict['nan']=np.nan


# In[7]:


homologar_bsa_dict


# In[8]:


bsa_total["Marca"] = "BSA" 


# In[9]:


bsa_total.columns


# In[10]:


#Extraemos de la base todos los que ya viene dentro de sus productos no null o nan 
bsa_limpia_1 = bsa_total[~bsa_total['Producto'].isna()]


# In[11]:


#Homologamos las familias y los productos
bsa_limpia_1["homologado"] = bsa_limpia_1["Producto"].map(homologar_bsa_dict)
bsa_limpia_1["familia"] = bsa_limpia_1["homologado"].map(homologar_bsa_familia_dict)


# In[12]:


bsa_limpia_1[bsa_limpia_1["homologado"].isna()]


# In[13]:


#Debemos ver dropna = false
#Debemos eliminar los que no tienen homologos 
bsa_limpia_1["homologado"].value_counts(dropna=False)


# In[14]:


#sacamos todos los productos que no tienen homologacion
bsa_limpia_2 = bsa_limpia_1[~bsa_limpia_1["homologado"].isna()]


# In[15]:


bsa_limpia_2["homologado"].value_counts(dropna=False)


# In[16]:


bsa_limpia_2["familia"].value_counts(dropna=False)


# In[17]:


bsa_limpia_2["Peso Neto"] = bsa_limpia_2["Peso Neto"].astype("int64")


# In[18]:


bsa_limpia_2


# In[19]:


bsa_total_agrup = bsa_limpia_2.groupby(by=["familia","Sucursal"],dropna=False).sum("Neto UF")
#bsa_total_agrup["Neto UF"].sort_values(ascending=False).to_excel(r"C:\Users\gonzalo.vera\OneDrive - Cementos BSA\Documentos\homologacion_precios\Agnos_anteriores\para_homol.xlsx")
bsa_total_agrup["Neto UF"].sort_values(ascending=False)


# In[20]:


bsa_limpia_2[bsa_limpia_2["familia"]=="ACUERDO COMERCIAL"]


# In[21]:


bsa_limpia_2[bsa_limpia_2["Región"]=="XV"]["Sucursal"]


# In[22]:


tabla = pd.pivot_table(bsa_limpia_2,values="Neto UF",index=["Región","Sucursal"],columns=["familia"],aggfunc=np.sum, fill_value=0)
tabla


# # Proceso Polpaico 21/22

# In[23]:


polp2023


# In[24]:


polp2023_limpia = polp2023[['Año Mes', 'Fecha de factura', 'ID Centro', 'ID Material', 'Material',
                                   'Cantidad facturada', 'Valor Neto de la posición', 'valor Ingreso UF',
                                   'Valor Unitario UF', 'Valor UF Actualidad']]
polp2023_limpia


# In[25]:


polp1y2.columns


# In[26]:


polp = pd.concat([polp1y2,polp2023_limpia])


# In[27]:


polp["ID Material"].unique()


# In[28]:


homologar_polp_dict = dict(zip(homol["ID Servicio Polpaico"],homol["Homologación"]))
homologar_polp_familias_dict = dict(zip(homol["Homologación"],homol["Grupo Servicio"]))
polp["homologado"] = polp["ID Material"].map(homologar_polp_dict)
polp["familia"] = polp["homologado"].map(homologar_polp_familias_dict)
homol.loc[54,["Grupo Servicio"]]="faenas nocturnas"


# In[29]:


polp[polp["familia"].isna()][["ID Material","Material"]].value_counts()


# In[30]:


polp_agrupado = polp.groupby(by="familia",dropna=False).sum("valor Ingreso UF")
polp_agrupado["valor Ingreso UF"].sort_values(ascending=False)


# In[31]:


bsa_total.shape


# In[32]:


bsa_total_region = bsa_total.groupby(by="Región",dropna=False).sum("Neto UF")
bsa_total_region["Neto UF"]


# In[33]:


bsa_total[bsa_total["Región"]=="I"].sort_values("Peso Neto",ascending=True)


# In[34]:


polp["ID Centro"].unique()


# In[35]:


polp["Marca"] = "Polpaico"


# In[36]:


polp


# In[37]:


url3 = r'C:\Users\ignacio.gutierrez\Cementos BSA\HBSA - Información Planificación Comercial\55. Data Analytics\1- Estrategia de Precios HPM\Servicios Complementarios\archivos_codigos\sucursales_polpaico.xlsx'

homol_suc = pd.read_excel(url3,sheet_name="Hoja1")


# In[38]:


homol_suc


# In[39]:


homol_suc["Cod_polp"] = homol_suc["Cod_polp"].astype(str).apply(lambda x:x.strip())
homol_suc["REGIONES"] = homol_suc["REGIONES"].astype(str).apply(lambda x:x.strip())
homol_suc["PLANTAS"] = homol_suc["PLANTAS"].astype(str).apply(lambda x:x.strip())
polp["ID Centro"] = polp["ID Centro"].astype(str).apply(lambda x:x.strip())


# In[40]:


homologar_suc_polp_dict = dict(zip(homol_suc["Cod_polp"],homol_suc["PLANTAS"]))
homologar_reg_polp_dict = dict(zip(homol_suc["Cod_polp"],homol_suc["REGIONES"]))


# In[41]:


homologar_suc_polp_dict


# In[42]:


homologar_reg_polp_dict


# In[43]:


polp["Región"] = polp["ID Centro"].map(homologar_reg_polp_dict)
polp["Región"]


# In[44]:


polp["Localidad"] = polp["ID Centro"].map(homologar_suc_polp_dict)
polp["Localidad"]


# In[45]:


#Aplicamos astype a estas columnas 
polp["Región"] =polp["Región"].astype(str).apply(lambda x:x.strip())
polp["Localidad"] =polp["Localidad"].astype(str).apply(lambda x:x.strip())


# In[46]:


polp["Localidad"].value_counts()


# In[47]:


polp["Región"].value_counts()


# In[48]:


polp_1 = polp[polp["Localidad"]!="0"]


# In[49]:


polp_2 = polp_1[polp_1["Localidad"]!="PPEE"]


# In[50]:


polp_2["Localidad"].value_counts()


# In[51]:


# Cambiar el nombre de la columna 'Año Mes' a 'Periodo'
polp_2= polp_2.rename(columns={'Año Mes': 'Periodo'})


# In[52]:


#Generar merge entre la tabla uf de registros con la uf de polpaico, ya que el registro de uf en polpaico no es acetivo.  
url4 = r'C:\Users\ignacio.gutierrez\Cementos BSA\HBSA - Información Planificación Comercial\43- Costeos Reales Polpaico\UF_IVP_UTM.xlsx'
valor_real_uf = pd.read_excel(url4,sheet_name="UF_IVP_UTM")


# In[53]:


valor_real_uf


# In[54]:


#merge entre UF real con base pol a partir de la fecha, utilizando left_merge

polp_3 = pd.merge(polp_2, valor_real_uf, on="Periodo" , how="left")


# In[55]:


print(polp_3.columns)


# In[56]:


polp_final = polp_3 [["Región","Localidad","familia","valor Ingreso UF","Unidad de fomento (UF) ","Periodo","homologado","Marca"]]


# In[57]:


polp_final["Unidad de fomento (UF) "] = polp_final["Unidad de fomento (UF) "].astype(float)


# In[58]:


ingresos_pesos = "Ingresos_pesos" 
polp_final["Unidad de fomento (UF) "] = polp_final["Unidad de fomento (UF) "].astype(float)
polp_final["ingresos_pesos"] = polp_final["valor Ingreso UF"] * polp_final["Unidad de fomento (UF) "]
polp_final["ingresos_pesos"] = polp_final["ingresos_pesos"].astype("int64")


# In[59]:


polp_final


# In[60]:


polp_final_2 = polp_final [["Región","Localidad","familia","ingresos_pesos","Periodo","homologado","Marca"]]
polp_final_2


# ## Analisis final

# In[61]:


bsa_final = bsa_limpia_2[["Región","Sucursal","familia","Periodo","Peso Neto","homologado","Marca"]]
bsa_final


# In[62]:


bsa_final = bsa_final.rename(columns={"Peso Neto": "ingresos_pesos"})
bsa_final


# In[63]:


polp_final_2


# In[64]:


bsa_final


# In[65]:


bsa_final_2 = bsa_final.rename(columns={"Sucursal":"Localidad"})


# In[66]:


bsa_final_2["Periodo"]


# In[67]:


consol_final = pd.concat([polp_final_2,bsa_final_2])


# In[68]:


consol_final = consol_final[consol_final["familia"]!="ACUERDO COMERCIAL"]


# In[69]:


consol_final


# In[70]:


consol_final.to_excel(r"C:\Users\ignacio.gutierrez\Cementos BSA\HBSA - Información Planificación Comercial\55. Data Analytics\1- Estrategia de Precios HPM\Servicios Complementarios\archivos_codigos\consolidado_Bi.xlsx")


# In[71]:


consol_final["Localidad"]=consol_final["Localidad"].apply(lambda x:x.upper())
consol_final["familia"]=consol_final["familia"].apply(lambda x:x.upper())
consol_final["ingresos_pesos"]=consol_final["ingresos_pesos"].astype("Int64")
consol_final["familia"] = consol_final["familia"].str.replace("MICELANEOS","MISCELANEOS")
consol_final


# In[72]:


consol_final["Localidad"].unique()


# In[73]:


consol_final["Periodo"] = consol_final['Periodo'].astype(str)


# In[74]:


# Convertir la columna 'fecha' al tipo datetime si no está en ese formato 
consol_final_2021 = consol_final[consol_final['Periodo'].str.contains('2021')]


# In[75]:


consol_final_2021


# In[76]:


consol_final_2021['ingresos_pesos'] = consol_final_2021['ingresos_pesos'].astype(float)


# In[77]:


#porcentaje_2022.to_excel(r"C:\Users\ignacio.gutierrez\Cementos BSA\HBSA - Información Planificación Comercial\55. Data Analytics\1- Estrategia de Precios HPM\Servicios Complementarios\archivos_codigos\Resultados_codigo_2021_2022\porcentaje_2022(02).xlsx")


# In[78]:


tabla1 = pd.pivot_table(
    consol_final_2021,
    values="ingresos_pesos",
    index=["Región","Localidad"],columns=["familia"],aggfunc=np.sum, fill_value=0, margins=True) 
pd.options.display.float_format = "{:,.0f}".format

tabla1


# In[79]:


get_ipython().system('pip install xlsxwriter')


# In[80]:


#tabla.to_excel(r'C:\Users\ignacio.gutierrez\OneDrive - Cementos BSA\Documentos\revision tablas.xlsx', index=False)


# In[81]:


columnas_convertir = ['ADICIONALES BOMBEO', 'APERTURA DE PLANTA', 'CARGA INCOMPLETA', 'EXTENSIÓN DE JORNADA', 'MUESTRAS ADICIONALES', 'SERVICIO BOMBEO', 'SOBREESTADÍA']

# Calcular los porcentajes de las columnas
tabla_porc_2021 = tabla1[columnas_convertir].apply(lambda x: (x / x.sum()) * 100)
tabla_porc_2021 = tabla_porc_2021.round(2)
tabla_porc_2021


# In[82]:


porcentaje_2021 = tabla_porc_2021.applymap(lambda x: '{}%'.format(float(x)))
porcentaje_2021


# In[83]:


consol_final_2022 = consol_final[consol_final['Periodo'].str.contains('2022')]


# In[84]:


consol_final_2022


# In[85]:


tabla2 = consol_final_2022
tabla2


# In[86]:


consol_final_2022['ingresos_pesos'] = consol_final_2022['ingresos_pesos'].astype(float)


# In[87]:


tabla2 = pd.pivot_table(
    consol_final_2022,
    values="ingresos_pesos",
    index=["Región","Localidad"],columns=["familia"],aggfunc=np.sum, fill_value=0, margins=True) 
pd.options.display.float_format = "{:,.0f}".format

tabla2


# In[88]:


tabla2.drop('All')


# In[89]:


columnas_convertir = ['ADICIONALES BOMBEO', 'APERTURA DE PLANTA', 'CARGA INCOMPLETA', 'EXTENSIÓN DE JORNADA', 'MUESTRAS ADICIONALES', 'SERVICIO BOMBEO', 'SOBREESTADÍA']

# Calcular los porcentajes de las columnas
tabla_porc2022= tabla2.drop('All')[columnas_convertir].apply(lambda x: (x / x.sum()) * 100)
#tabla_porc2022 = tabla_porc2022.round(2)
tabla_porc2022


# In[90]:


#sacar_totales_2022
totales = tabla2.sum(axis=0)
totales


# In[91]:


porcentaje_2022 = tabla_porc2022.applymap(lambda x: '{}%'.format(int(x)))

porcentaje_2022


# In[92]:


# Convertir la columna 'fecha' al tipo datetime si no está en ese formato 
consol_final_2023 = consol_final[consol_final['Periodo'].str.contains('2023')]
consol_final_2023['ingresos_pesos'] = consol_final_2023['ingresos_pesos'].astype(float)
tabla3 = consol_final_2023


# In[93]:


tabla3 = pd.pivot_table(
    consol_final_2023,
    values="ingresos_pesos",
    index=["Región","Localidad"],columns=["familia"],aggfunc=np.sum, fill_value=0, margins=True) 
pd.options.display.float_format = "{:,.0f}".format

tabla3


# In[94]:


columnas_convertir = ['ADICIONALES BOMBEO', 'APERTURA DE PLANTA', 'CARGA INCOMPLETA', 'EXTENSIÓN DE JORNADA', 'MUESTRAS ADICIONALES', 'SERVICIO BOMBEO', 'SOBREESTADÍA']

# Calcular los porcentajes de las columnas
tabla_porc2023= tabla3.drop('All')[columnas_convertir].apply(lambda x: (x / x.sum()) * 100)
#tabla_porc2023 = tabla_porc2023.round(2)
tabla_porc2023


# In[95]:


porcentaje_2023 = tabla_porc2023.applymap(lambda x: '{}%'.format(int(x)))

porcentaje_2023


# In[96]:


cd Downloads


# In[97]:


git clone https://github.com/Ignacio Gutiérrez S/Codigo_servicios_complementarios.git


# In[ ]:





# In[ ]:


#porcentaje_2021.to_excel(r"C:\Users\ignacio.gutierrez\Cementos BSA\HBSA - Información Planificación Comercial\55. Data Analytics\1- Estrategia de Precios HPM\Servicios Complementarios\archivos_codigos\Resultados_codigo_2021_2022\porcentaje_2021(01).xlsx")


# In[ ]:


#porcentaje_2022.to_excel(r"C:\Users\ignacio.gutierrez\Cementos BSA\HBSA - Información Planificación Comercial\55. Data Analytics\1- Estrategia de Precios HPM\Servicios Complementarios\archivos_codigos\Resultados_codigo_2021_2022\porcentaje_2022(02).xlsx")


# In[ ]:


#tabla1.to_excel(r"C:\Users\ignacio.gutierrez\Cementos BSA\HBSA - Información Planificación Comercial\55. Data Analytics\1- Estrategia de Precios HPM\Servicios Complementarios\archivos_codigos\Resultados_codigo_2021_2022\tabla2(02).xlsx")


# In[ ]:


#tabla2.to_excel(r"C:\Users\ignacio.gutierrez\Cementos BSA\HBSA - Información Planificación Comercial\55. Data Analytics\1- Estrategia de Precios HPM\Servicios Complementarios\archivos_codigos\Resultados_codigo_2021_2022\tabla1(01).xlsx")


# In[ ]:


#tabla3.to_excel(r"C:\Users\ignacio.gutierrez\Cementos BSA\HBSA - Información Planificación Comercial\55. Data Analytics\1- Estrategia de Precios HPM\Servicios Complementarios\archivos_codigos\Resultados_2023\tabla3(01).xlsx")


# In[ ]:


#porcentaje_2023.to_excel(r"C:\Users\ignacio.gutierrez\Cementos BSA\HBSA - Información Planificación Comercial\55. Data Analytics\1- Estrategia de Precios HPM\Servicios Complementarios\archivos_codigos\Resultados_2023\porcentaje_2023(01).xlsx")


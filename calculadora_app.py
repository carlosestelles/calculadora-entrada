'''
APLICACIÓN WEB CALCULADORA ENTRADA HIPOTECA
'''

### -----------------
# Importamos librerías
### -----------------
import pandas as pd
import numpy as np
from unidecode import unidecode

import streamlit as st

if 'municipios_provincia' not in st.session_state:
    st.session_state.municipios_provincia = []

if 'municipio' not in st.session_state:
    st.session_state.municipio = ''

if 'precio_municipio' not in st.session_state:
    st.session_state.precio_municipio = 0

### -----------------
# Definimos funciones
### -----------------

# Lee base de datos y la guarda en el caché para no leerla en cada rerun
@st.cache_data
def cargar_datos(file):
    '''Recibe el nombre del archivo .csv y lo carga como dataframe'''
    return pd.read_csv(file)

# Definimos resetear()
def resetear():
    '''Resetea parámetros de widgets y derivados'''
    st.session_state.provincia = ''
    st.session_state.municipio = ''
    st.session_state.municipios_provincia = []
    st.session_state.precio_municipio = 0


### -----------------
# Configuración web
### -----------------

# Definimos pestaña navegador
st.set_page_config(page_title="Calculadora Entrada Hipoteca", page_icon="🏠", layout="centered")

### -----------------
# WEB APP
### -----------------

# Títulos
st.title("¿Cuánto tardarías en ahorrar la entrada para un piso en tu ciudad?")
st.write("Elige tu municipio, salario y ahorros")

# Leemos base de datos
info_pueblos = cargar_datos('infopueblos.csv')

# Layout en 2 columnas
col1, col2 = st.columns(2)
with col1:
    # Seleccionamos provincia
    provincia = st.selectbox("Provincia", options=["A Coruña", "Álava", "Albacete", "Alicante", "Almería", "Asturias", "Ávila", "Badajoz", "Barcelona", "Burgos", "Cáceres", "Cádiz", "Cantabria", "Castellón", "Ceuta", "Ciudad Real", "Córdoba", "Cuenca", "Girona", "Granada", "Guadalajara", "Guipúzcoa", "Huelva", "Huesca", "Islas Baleares", "Jaén", "La Rioja", "Las Palmas", "León", "Lleida", "Lugo", "Madrid", "Málaga", "Melilla", "Murcia", "Navarra", "Ourense", "Palencia", "Pontevedra", "Salamanca", "Santa Cruz de Tenerife", "Segovia", "Sevilla", "Soria", "Tarragona", "Teruel", "Toledo", "Valencia", "Valladolid", "Vizcaya", "Zamora", "Zaragoza"],
                                              index = None, placeholder = 'Elige una provincia', key = 'provincia')
    
    prov_especiales = ["Islas Baleares", "Valencia", "León"]
    prov_corregidas = ["baleares", "valencia-provincia", "leon-provincia"]

    if provincia in prov_especiales:
        provincia = prov_corregidas[prov_especiales.index(provincia)]
    else:
        provincia = str(provincia)
        provincia = provincia.lower()
        provincia = provincia.replace(' ', '-')
        provincia = unidecode(provincia)

with col2:
    # Creamos la lista de municipios de esa provincia
    if provincia:
        st.session_state.municipios_provincia = info_pueblos.iloc[ info_pueblos['Provincia'].str.contains(provincia), 2]
    else:
        st.write("Por favor, selecciona provincia")

    # Seleccionamos municipio
    st.session_state.municipio = st.selectbox("Municipio", placeholder = 'Selecciona un municipio', options = st.session_state.municipios_provincia,
                                              index = None, key = f"municipio_{provincia}")
    st.session_state.municipio = str(st.session_state.municipio)
    
    # Buscamos precio m2 del municipio
    for i in range(len(info_pueblos)):
        if st.session_state.municipio == info_pueblos.iloc[i, 2]:
            st.session_state.precio_municipio = info_pueblos.iloc[i, 3]

col3, col4, col5 = st.columns(3)
with col3:
    salario = st.number_input('Sueldo neto mensual (€)',
                            value       = 1500,
                            min_value   = 1,
                            placeholder = "Salario",
                            width=160)

with col4:
    ahorro_porcen = st.number_input('Ahorro mensual (%)',
                            value       = 20,
                            min_value   = 1,
                            placeholder = "Porc ahorro",
                            width=160)
with col5:
    ahorros = st.number_input('Tus ahorros (€)',
                            value       = 0,
                            min_value   = 0,
                            placeholder="Dinero ahorrado",
                            width=160)

## CALCULOS
prec_piso = st.session_state.precio_municipio * 90
entrada = prec_piso * 0.3
entrada_real = entrada - ahorros
ahorro_mensual = salario * (ahorro_porcen / 100)
meses = entrada_real / ahorro_mensual
anyos = meses / 12

# Cálculo meses y años
column1, column2 = st.columns(2)
with column1:
    st.space("xxsmall")
    if st.session_state.municipio == 'None':
        st.subheader("Tardarías:")
    elif ahorros > entrada:
        st.subheader("Tienes suficiente ahorrado para la entrada🎈")
    else:
        st.subheader(f"Tardarías: {anyos:,.1f} años".replace(",", "@").replace(".",",").replace("@","."))

with column2:
    # Si queremos resetear valores
    st.space("small")
    st.button("Empezar de nuevo", on_click = resetear)

st.divider()

# Detalles
with st.expander('Mostrar detalles', type = 'compact'):
    st.write(f"Un piso de 90 m² en {st.session_state.municipio} cuesta {prec_piso:,.2f}€ de media y necesitas ahorrar {entrada_real:,.2f}€".replace(",", "@").replace(".",",").replace("@","."))
    # Ahorro mensual
    st.write(f"Tu ahorro mensual: {ahorro_mensual:,.2f}€".replace(",", "@").replace(".",",").replace("@","."))
    
    st.caption("Para calcular la entrada se suma el 20\% del valor del inmueble más un 10\% de gastos")

    # Fuente
    st.caption("Fuente precios: Idealista, septiembre 2026")
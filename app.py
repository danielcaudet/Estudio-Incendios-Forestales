import streamlit as st   # Después de instalar streamlit en mi entorno virtual, lo importo a mi archivo
import pandas as pd      # Importo pandas también pues me será necesario para trabajar los datos
import datetime          # Datetime para poder utilizar las fechas
import matplotlib        # Matplotlib será necesario a la hora de leer gráficas

st.set_page_config(         # Coloco el nombre y emoji de la página, el que se verá en la pestaña. 
    page_title = "Incendios forestales en España",
    page_icon = "🔥",
    layout = "wide"        # Elijo la anchura de mi web
)

@st.cache_data   

def cargar_datos():                # Cargo los datos de mis dos csv
    incendios = pd.read_csv("datos/incendios_limpios.csv")
    grandes_incendios = pd.read_csv("datos/grandes_limpios.csv")

    return incendios, grandes_incendios


incendios, grandes_incendios = cargar_datos()

st.write("En España contabilizamos", len(incendios), "incendios forestales, de los cuales", len(grandes_incendios), "son grandes incendios")


with st.sidebar:     # Aquí comienzo a colocar lo que quiero en las barras de la izquierda
    
    st.header("Filtros")  # El título
    comunidad = sorted(incendios["comunidad"].unique()) # Las comunidades por orden alfabético
    comunidad.insert(0, "Todas")  # Se añade todas cómo opción
    comunidad = st.selectbox("Comunidad", comunidad)

    provincia = sorted(incendios[incendios["comunidad"] == comunidad]["provincia"].unique())  # Hago lo mismo con las provincias, pero filtrandolas para que cada provincia salga dentro de la comunidad correspondiente
    provincia.insert(0, "Todas")
    provincia = st.selectbox("Provincia", provincia)

    causa = st.radio("Causa", ["Todas", "Causa Natural", "Negligencias y accidentes", "Intencionados", "Causa desconocida", "Reproducciones", "Otras causas humanas"])  # Una caja de selección para elegir la causa de los incendios que se buscan
    
    hectareas_min = st.number_input("Mínimo de hectáreas quemadas", min_value=0, max_value=29867, value=0, step=100)   # Con estos number_input, podré filtrar según el tamaño de los incendios
    hectareas_max = st.number_input("Máximo de hectáreas quemadas", min_value=0, max_value=29867, value=20867, step=100)   # Al ser números muy grandes de hecáreas, prefiero usar esto a un slider
    
    año_min, año_max = st.slider("Año", 1980, 2023, (1980, 2023))  # Utilizo un slider para poder filtrar los años

    meses = incendios.sort_values("numero mes")["mes"].unique().tolist()       # Otro para los meses, pero antes
    mes_min, mes_max = st.select_slider("Mes", options= meses, value = ("Enero", "Diciembre") )
    
    mes_min = meses.index(mes_min) + 1    # Vuelvo a convertir los meses en variables integrales para después poder utilizarlos en los filtrados
    mes_max = meses.index(mes_max) + 1



filtrados = incendios     # Comienzo a aplicar los filtros

if comunidad != "Todas":
    filtrados = filtrados[filtrados["comunidad"] == comunidad] # Selecciono con los incendios de la comunidad seleccionada

if provincia != "Todas":
    filtrados = filtrados[filtrados["provincia"] == provincia] # Lo mismo pero con la provincia

if causa!= "Todas":
    filtrados = filtrados[filtrados["causa"] == causa]   # Repito el proceso con la causa

filtrados = filtrados[(filtrados["hectareas"] >= hectareas_min)]
filtrados = filtrados[(filtrados["hectareas"] <= hectareas_max)]  # Ahora los incendios en con la cantida de hectáreas seleccionadas

filtrados = filtrados[(filtrados["año"] >= año_min)]   # Para finalizar, filtro los incendios por año y mes
filtrados = filtrados[(filtrados["año"] <= año_max)]

filtrados = filtrados[(filtrados["numero mes"] >= mes_min)]     
filtrados = filtrados[(filtrados["numero mes"] <= mes_max)]


if len(filtrados) == 0:      # Coloco un aviso para cuando el número de incendios filtrados sea 0
    st.warning("No existen incendios que coincidan con tu búsqueda")
    st.stop()    # Se para la ejecución para que no de error al calcular las métricas



col1, col2, col3, col4 = st.columns(4)      # Determino cuantas métricas voy a mostrar, una por columna

with col1:
    st.metric("Incendios", len(filtrados))  # El número de incendios filtrados
    
with col2:
    st.metric("Total de hectáreas quemadas", f"{int(filtrados['hectareas'].sum()):,}".replace(",", "."))   # Le añado puntos para que se vean os números con más claridad

with col3:
    st.metric("Media de hectáreas quemadas", filtrados["hectareas"].mean().round(1))   # Calculo la media de hectáreas quemadas de los incendios seleccionados
    
with col4: 
    impacto = filtrados["impacto economico"].sum()   # La última métrica que he elegido, el impacto económico mínimo.

    if impacto >= 1_000_000:
        impacto = f"{impacto / 1_000_000:.0f}M"
    else:
        impacto = f"{impacto:,.0f}".replace(",", ".")  # Añado los puntos para que los números se lean cn más claridad

    st.metric("Impacto económico mínimo", impacto)



tab1, tab2, tab3, tab4 = st.tabs (["Incendios", "Gráficas", "Mapa", "¿Cuanta probabilidad de verte afectado por un incendio forestal tienes?"])  # Comienzo con las pestañas

with tab1:      # En la primera pestaña muestro la tabla de incendios
    st.header("Los incendios filtrados")
    st.dataframe(filtrados)

with tab2:
    st.subheader("Número de incendios y hectáreas quemadas por comunidad")
    colx, coly = st.columns(2) # 3 columnas para los gráficos

    with colx:
        st.subheader("Incendios")
        com_afectadas = incendios["comunidad"].value_counts()
        st.bar_chart(com_afectadas, horizontal = True, height = 650, sort = "-count")

    with coly:
        st.subheader("Hectáreas")
        hect_quemadas = incendios.groupby("comunidad")["hectareas"].sum()
        st.bar_chart(hect_quemadas, horizontal = True, height = 650, sort = "-hectareas")

    st.subheader("Meses más peligrosos")

    

with tab3:   # En la tercera muestro el mapa de incendios filtrados
    st.header("Mapa de incendios")
    st.map(filtrados, latitude="latitud", longitude="longitud", size=20)


with tab4:
    pass
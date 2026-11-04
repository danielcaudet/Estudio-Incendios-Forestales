import streamlit as st   # Después de instalar streamlit en mi entorno virtual, lo importo a mi archivo
import pandas as pd      # Importo pandas también pues me será necesario para trabajar los datos
import datetime          # Datetime para poder utilizar las fechas
import altair as alt     # Altair será necesario para algunas gráficas

st.set_page_config(         # Coloco el nombre y emoji de la página, el que se verá en la pestaña. 
    page_title = "Incendios forestales en España",
    page_icon = "🔥",
    layout = "wide"        # Elijo la anchura de mi web
)

@st.cache_data   

def cargar_datos():                # Cargo los datos de mi csv
    incendios = pd.read_csv("datos/incendios_limpios.csv")
    
    

    return incendios


incendios = cargar_datos()

st.write("En España contabilizamos", len(incendios), "incendios forestales, de los cuales", len(incendios[incendios["hectareas"] >= 500]), "son grandes incendios")


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
    hectareas_max = st.number_input("Máximo de hectáreas quemadas", min_value=0, max_value=29867, value=29867, step=100)   # Al ser números muy grandes de hecáreas, prefiero usar esto a un slider
    
    año_min, año_max = st.slider("Año", 1968, 2023, (1968, 2023))  # Utilizo un slider para poder filtrar los años

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

    st.caption("* Los datos económicos son incompletos, por lo que no se recomienda utilizar esta cifra para realizar comparaciones.")



tab1, tab2, tab3, tab4 = st.tabs (["Incendios", "Gráficas", "Mapa", "Impacto en tu provincia"])  # Comienzo con las pestañas

with tab1:      # En la primera pestaña muestro la tabla de incendios
    st.header("Los incendios filtrados")
    st.dataframe(filtrados[["fecha", "comunidad","provincia", "municipio", "hectareas", "causa", "muertos"]])

    

    
with tab2:
    st.subheader("Número de incendios y hectáreas quemadas por comunidad")
    colx, coly = st.columns(2) # 3 columnas para los gráficos

    with colx:
        st.subheader("Incendios")
        com_afectadas = filtrados["comunidad"].value_counts()
        st.bar_chart(com_afectadas, horizontal = True, height = 650, sort = "-count")

    with coly:
        st.subheader("Hectáreas")
        hect_quemadas = filtrados.groupby("comunidad")["hectareas"].sum()
        st.bar_chart(hect_quemadas, horizontal = True, height = 650, sort = "-hectareas")

    
    st.subheader("Incendios por mes")

    meses = ["Enero", "Febrero", "Marzo", "Abril","Mayo", "Junio", "Julio", "Agosto","Septiembre", "Octubre", "Noviembre", "Diciembre"]
    # Primero coloco los nombres para que puedan salir en la gráfica, si no salfrán los números de mes
    meses_peligrosos = (filtrados.groupby("mes").size().reindex(meses, fill_value = 0).reset_index(name="Incendios"))
    # Creo la variable que utilizaré más adelante
    grafica = alt.Chart(meses_peligrosos).mark_line().encode(
        x=alt.X("mes:N", sort=meses, title="Mes", axis=alt.Axis(labelAngle= -45)),
        y=alt.Y("Incendios:Q", title="Número de incendios")).properties(height=450)

    # Preparo la gráfica y la represento con st.altair_chart
    st.altair_chart(grafica, use_container_width=True)

with tab3:   # En la tercera muestro el mapa de incendios filtrados
    st.header("Mapa de incendios")
    filtrados_mapa = filtrados.dropna(subset=["latitud", "longitud", "ubicación exacta"])  # Elimino los valores nulos
    st.map(filtrados_mapa, latitude="latitud", longitude="longitud", size=20)


with tab4:
    provincias = sorted(incendios["provincia"].dropna().unique())     # Preparo un selectbox para elegir la provincia
    provincia_elegida = st.selectbox("Selecciona tu provincia", provincias)
    
    datos_provincia = incendios[incendios["provincia"] == provincia_elegida]  # Filtro los datos de una provincia

    total_incendios = len(datos_provincia)     # Total de incendios de la provincia elegida
    total_hectareas = datos_provincia["hectareas"].sum()   # Total de hectáreas de la provincia elegida

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Número de incendios",total_incendios)

    with col2:
        st.metric("Hectáreas quemadas", int(total_hectareas))

    st.subheader("Media nacional por provincia")

    media_incendios = int(incendios["provincia"].value_counts().mean())    # Media nacional de incendios por provincia
    media_hectareas = int(incendios.groupby("provincia")["hectareas"].sum().mean())   # Media nacional de hectáreas quemadas por provincia
    

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Media de incendios", media_incendios)

    with col2:
        st.metric("Media de hectáreas", media_hectareas)

    if total_incendios > media_incendios and total_hectareas > media_hectareas:   # Preparo los distintos avisos según la comparación entre la provincia y la media sea más o menos favorable
        st.error(f"{provincia_elegida} ha sido más afectada que el resto")  # Utilizo st.error para los peores casos. Saldrá en rojo

    elif total_incendios < media_incendios and total_hectareas > media_hectareas:  # St.warning para casos intermedios, en que sólo una de las dos cantidades supera a la media nacional. Saldrá en amarillo
        st.warning(f"{provincia_elegida} ha sufrido menos incendios que la media, pero han sido más extensos")

    elif total_incendios > media_incendios and total_hectareas < media_hectareas:
        st.warning(f"{provincia_elegida} ha sufrido más inendios que la media, pero han sido menos extensos")

    elif total_incendios < media_incendios and total_hectareas < media_hectareas:   # St.success para las provincias menos afectadas. Saldrá en verda
        st.success(f"{provincia_elegida} ha sido menos afectada que la media")   

    st.subheader("Gráfica comparativa de incendios")

    evolucion_provincia = datos_provincia["año"].value_counts().sort_index()   # Calculo la evolución de la provincia
    evolucion_nacional = incendios["año"].value_counts().sort_index() / incendios["provincia"].nunique()   # Calculo la evolución media

    comparacion = pd.DataFrame({provincia_elegida : evolucion_provincia, "Media" : evolucion_nacional})    # Las coloco en un mismo dataframe

    st.line_chart(comparacion, color = ["red", "blue"])     # Muestro el dataframe, eligiendo los colores de las líneas

    st.subheader("Gráfica comparativa de hectáreas quemadas")

    evolucion_hectareas_provincia = datos_provincia.groupby("año")["hectareas"].sum().sort_index()

    evolucion_hectareas_nacional = incendios.groupby("año")["hectareas"].sum().sort_index() / incendios["provincia"].nunique()

    comparacion_hectareas = pd.DataFrame({provincia_elegida: evolucion_hectareas_provincia,"Media": evolucion_hectareas_nacional})

    st.line_chart(comparacion_hectareas, color=["red", "blue"])
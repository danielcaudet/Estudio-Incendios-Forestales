# Título del proyecto

Una frase: qué es y para quién.

Análisis de los incendios forestales en España, dirigido a encargados de la administración pública relacionados con el medio ambiente, así cómo al público general.

## La pregunta

¿Cómo han evolucionado los incendios forestales en España y que territorios han sido los más afectados?

## Los datos

- De dónde salen: (https://datos.civio.es/dataset/todos-los-incendios-forestales/)
- Cuántos son: 296.839 filas y 21 columnas
- Qué es cada fila: Un incendio

## Qué he limpiado y por qué

- Se ha eliminado las columnas de id y id de municipio, ya que no aportaban información interesante.
- La columna de causa desclasificada era una división más específica de la columna causa, la he eliminado porque creo que causa es más visual y entendible para un receptor que no sea especialista en la materia. Se podria recuperar la columna en caso de redirigir el proyecto para hacerlo más específico.
- En la columna de tiempo de control faltaban demasiados datos, así que se ha eliminado.
- La columna de tiempo de extinción se ha eliminado. Era interesante, pero por si sola no aportaba mucha información. Con más datos de tiempo de control, o encontrando datos de prevención de incendios, por ejemplo, se podría aprovechar. 
- Se han eliminado los incendios duplicados al ser un número muy pequeño.
- Un 18% de incendios no tenían los datos de latitud y longitud. Se han mantenido en la tabla para poder analizar el máximo número de inendios posible, pero se han eliminado en el momento de mostrarlos en el mapa.
- Los datos económicos sirven para hacerse una idea del gasto causado cómo mínimo, pero la falta de datos en este campo impide sacar más conclusiones.

## Lo que he encontrado

1. Los grandes incendios tienen un impacto muy importante. De los registros analizados, 2.162 corresponden a grandes incendios, que acumulan aproximadamente 3,32 millones de hectáreas quemadas. Aunque representan solamente el 0,73 % del total de incendios, concentran aproximadamente el 41 % de la superficie quemada.
2. Agosto es el mes más afectado, con aproximadamente 2,47 millones de hectáreas quemadas, seguido de Julio, con 1,74 millones, y Septiembre, con 1,34 millones.
3. Galicia concentra aproximadamente el 35,6 % de los incendios registrados, seguida de Castilla y León (15,8 %) y Asturias (11,6 %).
4. El número de incendios ha cambiado a lo largo del tiempo. Las décadas de 1980 y 1990 concentran un número especialmente elevado de registros. En las décadas posteriores se observa una reducción respecto a esos máximos, aunque la evolución no es constante.
5. La evolución de la superficie quemada también presenta importantes diferencias entre periodos, aunque sigue habiendo años con incendios especialmente graves. La media de hectáreas quemadas por incendio era de 42.9 y 44.6 en las décadas de los 60 y los 70, y se fue reduciendo hasta la década del 2000 con 18.7. En la década de 2010 vuelve a subir con 24.3.

## La app

![La app](capturas/app.png)

La aplicación permite consultar la evolución histórica de los incendios y filtrar estos por comunidad, provincia, tamaño, causa, año y mes. Se pueden visualizar en el mapa y finalmente se puede observar el impacto de los incendios en la provincia que se elija.

Enlace: (si la has publicado en Streamlit Community Cloud)

## Cómo ejecutarlo

1. Crear un entorno e instalar las librerías: `pip install -r requirements.txt`
2. El EDA está en `eda.ipynb`.
3. La app se abre con `streamlit run app.py`.

## Autor

Daniel Caudet Ruiz
https://github.com/danielcaudet

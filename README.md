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

1. De los registros analizados, 2.162 corresponden a grandes incendios, que acumulan aproximadamente 3,32 millones de hectáreas quemadas. A pesar de representar una proporción muy pequeña del total, su impacto territorial es considerable.
2. Agosto es el mes más afectado, con aproximadamente 2,47 millones de hectáreas quemadas, seguido de julio, con 1,74 millones, y septiembre, con 1,34 millones.
3. Galicia concentra aproximadamente el 35,6 % de los incendios registrados, seguida de Castilla y León (15,8 %) y Asturias (11,6 %).

## La app

![La app](capturas/app.png)

(Qué se puede hacer en la app, en dos o tres frases.)

Enlace: (si la has publicado en Streamlit Community Cloud)

## Cómo ejecutarlo

1. Crear un entorno e instalar las librerías: `pip install -r requirements.txt`
2. El EDA está en `eda.ipynb`.
3. La app se abre con `streamlit run app.py`.

## Autor

Daniel Caudet Ruiz
https://github.com/danielcaudet

recetas_prompt = """
Usando los datos que voy a pasarte debes generar una conclusión similar. Te paso un ejemplo previo de como deberían ser las conclusiones en estructura y longitud y los datos. EJEMPLOS PREVIOS:

Este indicador estima si en una farmacia hay un número significativo de recetas sin conciliar, ya que esto puede indicar que se estén usando recetas ficticias para cuadrar stock y/o caja  para encubrir movimientos fraudulentos.  Las cifras que deben analizarse, junto con su distribución por usuario y mes, son las siguientes:

- Cuantas recetas hay sin conciliar
- El porcentaje de recetas sin conciliar sobre el total
- La distribución de las recetas sin conciliar por tipo de aportación

Para los usuarios usa solo dos números para cada uno: 1. Porcentaje del total de recetas sin conciliar. 2. Número de recetas sin conciliar

Se debe analizar la evolución a lo largo del tiempo con el fin de identificar tendencias o patrones

ASEGURATE DE USAR EXACTAMENTE LOS DATOS QUE ESTÁN EN EL APARTADO 'TEXTO CON LOS DATOS PARA REDACTAR LA CONCLUSION'
EVITA USAR LAS PALABRAS 'En conclusion'

Añade un pequeño párrafo sobre la evolución del indicador en el último més, normalmente no habrá cambios significativos, pero es importante nombrarlo, por ejemplo, para cambios poco relevantes:
En el último mes no ha habido cambios significativos en los valores del indicador.

Ejemplo 1:
En conclusión, se trata de un indicador totalmente bajo control.


A lo largo del periodo de estudio se han registrado 113.328 recetas, de las cuales únicamente ha quedado una sin conciliar.


La única receta sin conciliar es de “XIGDUO 5/850 MG 56 COMPRIMIDOS RECUBIERTOS”, aportación tipo X0, vendido por el usuario 43 (titular) el 29 de enero de 2024.


Ejemplo 2:

El uso inapropiado de las recetas durante las ventas puede ocurrir de cara a ocultar irregularidades. El análisis muestra un 0,04% de recetas no conciliadas, que supone un total de 136 recetas.



Estas cifras no son especialmente elevadas, pero destacan los siguientes usuarios:



Usuario 2: el que tiene mayor nº de  recetas sin conciliar (29) y el segundo que más en los últimos 3 meses (9).


Usuario 4: Actúa muy poco en mostrador, pero dejó 3 recetas sin conciliar en enero (7,69% de su total).


Usuario 5: el que en más nº de meses distintos ha dejado recetas sin conciliar (13 meses frente a 5-8 de sus compañeros). Es también el que mayor porcentaje tiene (0,08%).


Usuario 6: el que más recetas ha dejado sin conciliar en los últimos 3 meses (10).


Usuario 7: 27 recetas sin conciliar; 0,07% de su total.


Es importante revisar si lo comentado se puede justificar con la operativa de la farmacia.

(Para los decimales usa comas y para los miles usa los puntos)
(Si aparece el usuario -1, cambia su nombre por usuario administrador, no uses 'el usuario -1')

DATOS PARA REDACTAR UNA CONCLUSION SIMILAR PARA ESTA FARMACIA:

"""
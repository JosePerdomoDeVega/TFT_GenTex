devs_prompt = """
Usando los datos que voy a pasarte debes generar una conclusión similar.

Este indicador estima si en una farmacia hay demasiadas operaciones de devolución, si se concentran en usuarios en concreto, y si se relacionan con algún patrón sospechoso en concreto. Las cifras que deben analizarse, junto con su distribución por usuario y mes, son las siguientes:

- Número de unidades devueltas
- Importe neto total de las devoluciones
- Precio medio de las devoluciones
- Ratio de devoluciones

Se debe analizar la evolución a lo largo del tiempo con el fin de identificar tendencias o patrones

ASEGURATE DE USAR EXACTAMENTE LOS DATOS QUE ESTÁN EN EL APARTADO 'TEXTO CON LOS DATOS PARA REDACTAR LA CONCLUSION'
EVITA USAR LAS PALABRAS 'En conclusion'

Añade un pequeño párrafo sobre la evolución del indicador en el último més, normalmente no habrá cambios significativos, pero es importante nombrarlo, por ejemplo, para cambios poco relevantes:
En el último mes no ha habido cambios significativos en los valores del indicador.

Te paso un ejemplo previo de como deberían ser las conclusiones en estructura y longitud y los datos. EJEMPLO PREVIO: La cantidad de devoluciones, su importe, así como el precio medio por devolución son señales a vigilar. En este caso se observa un total de 95.359,59€ en devoluciones, lo cual se considera un importe exageradamente elevado. Del mismo modo, el número de unidades devueltas (15.738) es excesivamente elevado.

Tras observar el detalle de las operaciones, hemos detectado una irregularidad que explica en gran medida las cifras globales elevadas: un elevado número de devoluciones de alto importe bajo el concepto “BILLETES 5.00€”. Esto, aún en caso de estar controlado por la titular, puede ser una fuente de otro tipo de irregularidades. Además, “intoxica” el resto de datos para su correcto análisis.

El mayor número de unidades devueltas lo presenta el usuario 10 (4.947). Le siguen el usuario 3 con 3.886 y el usuario 7 con 2.815.

Respecto a importe de dichas devoluciones, vuelve a destacar el usuario 10, con 24.115€ en devoluciones. De nuevo le sigue el usuario 3 (21.559€) y, a continuación, el usuario 7 con 14.090€.

El precio medio de las devoluciones en la farmacia es de 6,06€. En este campo, el valor más alto lo presenta el usuario 2 con 12,34€. Le siguen el usuario 6 (11,43€) y el usuario 8 (9,83€).

El ratio de devoluciones medio en esta farmacia es del 1,84%, la cual es una cifra bajo control. Sin embargo, el usuario 10 presenta un ratio drásticamente elevado (6,11%). También son elevados los ratios del usuario 6 (3,06%), el usuario 4 (2,78%) y el usuario 3 (2,29%).

En cuanto a tendencias, se ha detectado un mayor importe de devoluciones del usuario 3 entre septiembre de 2021 y mayo de 2022; y un menor importe de devoluciones del usuario 7 desde marzo de 2022.

En conclusión, la farmacia presenta unas cifras globales de importe en devoluciones y número de unidades devueltas excesivamente elevadas. Esto se debe en gran medida a las operaciones bajo el concepto “BILLETES 5.00€”, las cuales son irregulares e intoxican el resto de datos. Destaca principalmente el usuario 10, por su importe, nº de unidades devueltas y ratio. En un escalón inferior, también destacan los usuarios 3, 7, 2 y 6.

(Para los decimales usa comas y para los miles usa los puntos)
(Si aparece el usuario -1, cambia su nombre por usuario administrador, no uses 'el usuario -1')

TEXTO CON LOS DATOS PARA REDACTAR LA CONCLUSION:



"""
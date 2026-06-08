stock_prompt = """
Usando los datos que voy a pasarte debes generar una conclusión similar. Te paso un ejemplo previo de como deberían ser las conclusiones en estructura y longitud y los datos. EJEMPLO PREVIO:

Este indicador estima si en una OF hay un volumen de cambios de stock elevado, que podría indicar que se está intentando encubrir desviaciones de medicamentos o productos, tras haber cometido un acto fraudulento.  Las cifras que deben analizarse, junto con su distribución por usuario y mes, son las siguientes:

- Número de operaciones de cambios de stock
- Variación de unidades del stock
- Distribución del número de operaciones y de variación de unidades por motivo de cambio de stock

Es importante vigilar especialmente las del motivo “Stock Manual”. Los cambios elevados de stock por motivo “Devolución Venta” son normales en farmacias con un alto número de devoluciones.

Se debe analizar la evolución a lo largo del tiempo con el fin de identificar tendencias o patrones

ASEGURATE DE USAR EXACTAMENTE LOS DATOS QUE ESTÁN EN EL APARTADO 'TEXTO CON LOS DATOS PARA REDACTAR LA CONCLUSION'
EVITA USAR LAS PALABRAS 'En conclusion'

Añade un pequeño párrafo sobre la evolución del indicador en el último més, normalmente no habrá cambios significativos, pero es importante nombrarlo, por ejemplo, para cambios poco relevantes:
En el último mes no ha habido cambios significativos en los valores del indicador.

Ejemplo 1:


En conclusión, hay un número muy elevado de cambios de stock y de variación de unidades en la farmacia. Los motivos más preocupantes son el 1 (”Stock Manual”) y el 20 (”Devolución Recepción”), donde además del usuario administrador, destaca la presencia del usuario 12. Por otro lado, el usuario 89, marcado como no empleado en el cuestionario, es el responsable de un gran número de variaciones fruto de un inventario en junio de 2024.

Se observan 53.344 operaciones de cambio de stock, las cuales han dado lugar a una variación de 70.261 unidades. Se trata de cifras muy elevadas.

El usuario 89 es el que realiza el 25% de los cambios de stock de la farmacia y en el cuestionario se ha indicado que no es un empleado. Se corresponde en su mayoría con un inventario realizado en junio de 2024.

Además del usuario mencionado en el punto anterior y el 43 (titular), también han realizado cambios de stock el usuario 12 y el usuario 65. Es importante revisar si esto encaja con la operativa de la farmacia.

Destaca en primer lugar el motivo 1 (”Stock Manual”) con 3.257 operaciones, las cuales han dado lugar a una variación de 5.304 unidades. El 52% han sido realizadas por el usuario 12; el 43% por el titular; y el 6% por el usuario administrador.

Destaca también el motivo 20 (”Devolución Recepción”) con 6.676 operaciones, las cuales han dado lugar a una variación de 10.541 unidades. El 100% han sido realizadas por el usuario administrador.




Aquí tienes la tabla de los valores de los diferentes motivos de cambio de stock

ID   Descripción
9    Cambio de Codigo
39   Control Stock (S.A.C.S.)
20   Devolucion Recepcion
21   Devolucion Recetas
19   Devolucion Venta
11   Edicion de Receta Manual
22   Inventario
31   Ordenes de Traspaso
26   Receta Borrada
1    Stock Manual
35   Stock Manual


Asegurate de incluir el porcentaje que representa cada usuario sobre el total de cambios de stock.

(Para los decimales usa comas y para los miles usa los puntos)
IMPORTANTE --> (Si aparece el usuario -1, cambia su nombre por 'usuario administrador', no uses 'el usuario -1' ni el '-1' para referirte a él.)

TEXTO CON LOS DATOS PARA REDACTAR LA CONCLUSION:



"""
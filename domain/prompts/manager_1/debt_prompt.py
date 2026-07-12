debt_prompt = """
Usando los datos que voy a pasarte debes generar una conclusión similar. Te paso un ejemplo previo de como deberían ser las conclusiones en estructura y longitud y los datos. EJEMPLO PREVIO:

Este indicador estima si en una farmacia se genera deuda de forma recurrente y fuera  la operativa de la farmacia, estudiando si hay clientes y/o empleados recurrentes a los que se asocia la deuda.  Las cifras que deben analizarse, junto con su distribución por usuario y mes, son las siguientes:

- Deuda generada o saldada en el periodo de estudio
- Deuda total antes del periodo de estudio
- Deuda total después del periodo de estudio
- Cantidad y porcentaje de deuda que suponen las recetas pendientes
- Número de clientes que han generado y/o saldado deuda en la farmacia

También debe analizarse la evolución y tendencia de la deuda total de la farmacia; así como el comportamiento de la deuda de clientes con patrones extraños, como, por ejemplo, los clientes que generan deuda pero nunca la saldan.

Se debe analizar la evolución a lo largo del tiempo con el fin de identificar tendencias o patrones

IMPORTANTE --> **IGNORA LAS CUENTAS DE LOS TITULARES, NO LAS NOMBRES EN TU RESPUESTA BAJO NINGÚN CONCEPTO, NO DIGAS NADA SOBRE ELLAS (Aquellas que comienzan por Tit.) NO LAS TENGAS EN CUENTA**

ASEGURATE DE USAR EXACTAMENTE LOS DATOS QUE ESTÁN EN EL APARTADO 'TEXTO CON LOS DATOS PARA REDACTAR LA CONCLUSION'
EVITA USAR LAS PALABRAS 'En conclusion'

Añade un pequeño párrafo sobre la evolución del indicador en el último més, normalmente no habrá cambios significativos, pero es importante nombrarlo, por ejemplo, para cambios poco relevantes:
En el último mes no ha habido cambios significativos en los valores del indicador.

Ejemplo 1:

En conclusión, la deuda histórica es drásticamente elevada. En el periodo de estudio ha aumentado en 2.704,54€. Destaca el protagonismo del usuario 87 generando deuda y el del usuario 12 saldando deuda. Por último, destaca que 115 cuentas de cliente hayan tenido movimientos cuando solo deberían tener movimientos cuentas de clientes para empleados.
En el periodo de estudio ha aumentado la deuda en 2.704,54€, lo cual es un importe moderado.
La deuda acumulada es drásticamente elevada (339.020€). Es importante revisar si esta deuda ha sido saldada de una forma que no quede reflejada en el programa de gestión.
De esa deuda acumulada, corresponden con recetas pendientes 18.633€, lo cual supone un 5,5% del total.
Destaca que 115 cuentas de cliente hayan generado/saldado deuda en el periodo de estudio, dado que en el formulario se respondió que solo los empleados pueden hacerlo. Solo en el 2024 han tenido movimientos 70 cuentas, una cifra superior a la de años anteriores.
Destaca notablemente la cuenta G0001, dado que es la que más deuda ha saldado en el periodo de estudio y, sin embargo, la que más deuda ha generado en el 2024. Es la cuenta más relevante de la farmacia, la que más influye en la tendencia general.
Tanto en la segunda mitad de 2022 como ligeramente en el 2023 se logró disminuir la deuda de la farmacia. Sin embargo, en esta primera mitad de 2024 ha aumentado en 4.821€. Se puede apreciar claramente en la línea de evolución de la farmacia.
El usuario 87 es el que más deuda genera en la farmacia (12.001€), con una diferencia notable sobre los siguientes (usuario 74 con 3.259€ y usuario 100 con 1.822€).
Los usuarios 43 (titular) y 12 son, con diferencia, los que más deuda saldan, con 10.366€ y 6.357€ respectivamente. Es importante revisar si esta actividad del usuario 12 se corresponde con la operativa normal de la farmacia.



Ejemplo 2:

Antes de comenzar el periodo de estudio, la deuda de la farmacia era de 70.570,39€. En los dos últimos años se ha reducido en 1.183,83€, dejando la deuda de clientes total actual de la farmacia en 69.386,56€.
Para entender correctamente las cifras de este indicador, es importante tener en cuenta que lo que se está midiendo es lo ocurrido en el periodo de estudio (2 años), y que las cantidades de deuda registradas por uno o varios usuarios puede ser superior al total del periodo porque otros usuarios únicamente hayan registrado deuda que se salda (y ello lo compense lo anterior). De igual forma ocurre con las cuentas de clientes.
También es importante tener en cuenta que actualmente no se está excluyendo del análisis a las cuentas de cliente de los empleados de la farmacia.
De las 909 cuentas de clientes que han generado deuda con la farmacia en el periodo de estudio (una cantidad bastante elevada), las cuentas 1766, 8 y 1667 son las tres primeras en el ranking de clientes que más deuda han acumulado.
Destaca principalmente la cuenta 1766, tanto por ser la que encabeza con diferencia el ranking de deuda (1.536,74€), como por tener una tendencia siempre creciente de su deuda y saldando cantidades en escasas ocasiones. La mayoría de la deuda de esta cuenta la ha registrado el usuario 9.
Se pueden observar tendencias similares a la mencionada anteriormente en las cuentas 8, 1667 y 162.
Destaca notablemente el usuario 2 por ser el que más deuda registran a los clientes de la farmacia. En un segundo escalón se encuentran los usuarios 9 y 6. Conviene revisar si esto tiene sentido con la operativa normal de la farmacia.


IMPORTANTE:

--Los usuarios o cuentas de cliente con valor -9999 o -1111 (en general numeros negativos de 4 cifras) son del total de la tienda, no lo tengas en cuenta a la hora de redactar sobre usuarios o cuentas de cliente.


(Para los decimales usa comas y para los miles usa los puntos)
(Si aparece el usuario -1, cambia su nombre por usuario administrador, no uses 'el usuario -1')

TEXTO CON LOS DATOS PARA REDACTAR LA CONCLUSION:


"""
cp_prompt = """
Usando los datos que voy a pasarte debes generar una conclusión similar. Te paso un ejemplo previo de como deberían ser las conclusiones en estructura y longitud y los datos. EJEMPLOS PREVIOS:
NO HAGAS TU CONCLUSION EXCESIVAMENTE E INNECESARIAMENTE LARGA PERO USA TODOS LOS DATOS QUE SE TE PROPORCIONAN.
Este indicador estima si en una OF se están realizando muchas devoluciones usando como código de producto un código que no corresponda con un producto de venta en la farmacia, como promociones, bolsas, servicios, etc. Al no modificar el stock en muchos casos, estos códigos pueden usarse para cometer movimientos fraudulentos.  Las cifras que deben analizarse, junto con su distribución por usuario y mes, son las siguientes:

- Número de unidades devueltas de productos con códigos propios
- Distribución del número de unidades devueltas por códigos propios más destacados
- Importe neto total de las devoluciones con códigos propios
- Precio medio de las devoluciones con códigos propios
- Ratio de devoluciones con códigos propios

Para una mayor seguridad y control de las operaciones, es recomendable no reutilizar códigos (es decir, que cada código propio de la farmacia se utilice para un único concepto).

Se debe analizar la evolución a lo largo del tiempo con el fin de identificar tendencias o patrones

ASEGURATE DE USAR EXACTAMENTE LOS DATOS QUE ESTÁN EN EL APARTADO 'TEXTO CON LOS DATOS PARA REDACTAR LA CONCLUSION'
EVITA USAR LAS PALABRAS 'En conclusion'

Añade un pequeño párrafo sobre la evolución del indicador en el último més, normalmente no habrá cambios significativos, pero es importante nombrarlo, por ejemplo, para cambios poco relevantes:
En el último mes no ha habido cambios significativos en los valores del indicador.

Ejemplo 1:

En conclusión, estamos ante un indicador con cifras moderadas cuando aplicamos el filtro para eliminar los descuentos por Tarjeta Trébol Plus. Sin embargo, es importante revisar los movimientos destacados de los usuarios 12, 43 y 74, así como verificar que sea correcta la operativa seguida para las VENTAS VARIAS bajo los códigos 64989 y 64990. Además, es importante tener un único concepto por cada código propio para evitar riesgos.


Al igual que en el indicador de devoluciones, es necesario filtrar y quitar la categoría “Marketing” para no incluir en el análisis a los descuentos de la Tarjeta Trébol Plus como devoluciones con códigos propios.


Los dos códigos propios más utilizados (64989 y 64990) se corresponden con conceptos de VENTAS VARIAS. Es importante revisar estas operaciones.


Destaca negativamente la reutilización de códigos propios (p.e. el 500017), lo cual complica el correcto seguimiento y es una fuente de riesgos.


Podemos observar un pico muy pronunciado en octubre de 2022. Se debe a dos devoluciones del usuario 12 bajo el concepto “ABONO DEVOLUCIÓN” por valor de 456,31€ ambos. Este usuario es el que presenta mayor importe (1.045€) y precio medio (87,07€) en este indicador.


También destaca notablemente la devolución del usuario 74 en febrero de 2024 de “VYDURA 75 MG” por valor de 200,25€. Este usuario destaca además porque realiza el 25% de devoluciones con códigos propios de toda la farmacia.


También destaca el usuario 43 (titular), por un elevado precio medio de las devoluciones (47,04€ frente a una media de 20,60€), lo cual le convierte en el segundo usuario con mayor importe en devoluciones con códigos propios de la farmacia.


El ratio de devoluciones con códigos propios en 2024 es del 0,05%, cuando los dos años anteriores ha sido del 0,03%.


La media mensual disminuyó drásticamente de 2022 a 2023. Sin embargo, entre 2023 y 2024 ha vuelto a aumentar.


(Para los decimales usa comas y para los miles usa los puntos)
(Si aparece el usuario -1, cambia su nombre por usuario administrador, no uses 'el usuario -1')

CUANDO USES EL CODIGO DE UN PRODUCTO PARA HABLAR DE EL, NOMBRA LA DESCRIPCION DEL PRODUCTO

TEXTO CON LOS DATOS PARA REDACTAR LA CONCLUSION:

"""
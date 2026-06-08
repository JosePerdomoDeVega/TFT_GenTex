pvp_prompt = """
Usando los datos que voy a pasarte debes generar una conclusión similar sobre este indicador sobre la situación actual de una farmacia.

Este indicador estima si en una farmacia hay demasiados cambios de precio a la baja en entornos en los que no debería, y estimar su impacto en base a la operativa de la OF.  Las cifras que deben analizarse, junto con su distribución por usuario y mes, son las siguientes:

- Número de operaciones de cambios de precio
- Distribución del número de operaciones de cambios de precio a la baja por entorno de ventas
- Importe total de cambios de precio a la baja
- Valor medio del cambio de precio a la baja
- Ratio de cambios de precio

Se debe analizar la evolución a lo largo del tiempo con el fin de identificar tendencias o patrones

IMPORTANTE ----> SIEMPRE SIEMPRE SIEMPRE los datos del entorno 2 (Ficha) serán muy superiores a los del resto de entornos por lo tanto no digas lo evidente (que los datos del entorno 2 son superiores al resto), habla brevemente del entorno 2 y comenta algo más a fondo el resto de entornos de la farmacia que tengan datos.
CUANDO NOMBRES EL ENTORNO, DI LA DESCRIPCION DEL MISMO. Ejemplo: entorno 2 ("Ficha")

ASEGURATE DE USAR EXACTAMENTE LOS DATOS QUE ESTÁN EN EL APARTADO 'TEXTO CON LOS DATOS PARA REDACTAR LA CONCLUSION'
EVITA USAR LAS PALABRAS 'En conclusion'

Añade un pequeño párrafo sobre la evolución del indicador en el último més, normalmente no habrá cambios significativos, pero es importante nombrarlo, por ejemplo, para cambios poco relevantes:
En el último mes no ha habido cambios significativos en los valores del indicador.


Te paso un ejemplo previo de como deberían ser las conclusiones en estructura y longitud y los datos. EJEMPLO PREVIO:
En conclusión, el indicador presenta cifras generales moderadas-elevadas en las que destacan principalmente las VENTAS VARIAS IVA X%. Destaca especialmente el usuario 12 tanto por importe como por número de operaciones propias de un usuario con más movimientos en la farmacia (lo cual resulta en un ratio muy alejado de la media), además de un precio medio de los cambios de PVP que supera los 18€ (alejado de la media). En cuanto a ratio, también destacan los usuarios 100 y 74; mientras que en precio medio destacan los usuarios 74, 100, 103, 43 y 90.

En el entorno 1 (”Ventas a PVP”), tanto el número de descuentos con cambios de PVP  (257) como el importe total descontado en esas operaciones (3.515€) son moderados-elevados.

El valor medio de los descuentos (13,68€) es elevado. Destaca especialmente el de los usuarios 74 (18,36€), 12 (18,17€), 103 (18,19€) y 100 (15,99€). En este año 2024, el del usuario 100 es de 19,42€; el del usuario 43 es de 23,55€; el del usuario 103 de 18,19€; y el del 90 de 26,85€.

El valor medio de los descuentos disminuyó entre 2022 y 2023, pero ha vuelto a aumentar en 2024.

La mayoría de los cambios de precio de mayor cuantía son bajo el concepto VENTAS VARIAS IVA X% y FORMULAS CAPSULAS. Lo primero debe revisarse si encaja con la operativa de la farmacia.

Destaca especialmente que el usuario 12 esté entre aquellos con más operaciones e importe, dado que no es uno de los que más movimientos realiza en la farmacia.

El ratio general de cambios de PVP de la farmacia (0,07%) está bajo control. Sin embargo, se aleja drásticamente el ratio del usuario 12 (0,19%). También se aleja, más moderadamente, el usuario 100 (0,11%). En el 2024, el usuario 74 tiene un ratio del 0,15% y el usuario 100 del 0,13%. El del usuario 12 en 2022 era del 0,26%.

El ratio general ha ido aumentando a lo largo de los años. 0,05% en 2022; 0,07% en 2023; y 0,08% en 2024.

En el entorno 2 (”Ficha”), nos encontramos con unas cifras muy elevadas: 5.021 operaciones de cambio de precio por un valor de 29.573€ descontados.

Solo dos usuarios-empleados hacen cambios de precio en este entorno: el usuario 12 (42 operaciones por valor de 643€ descontados) y el usuario 43 (15 operaciones por valor de 245€). El resto de operaciones e importe () corresponde con el usuario administrador.

El cambio de PVP medio en este entorno es de 5,69€, notablemente inferior a los 13,68 del entorno de “Ventas a PVP”.

Sin embargo, el ratio se dispara hasta el 2,4%.
-------------------------------------------------------------------------------------------------------------------------------
(Para los decimales usa comas y para los miles usa los puntos)
(Si aparece el usuario -1, cambia su nombre por usuario administrador, no uses 'el usuario -1')

TEXTO CON LOS DATOS PARA REDACTAR LA CONCLUSION:

"""
stock_prompt = """
Usando los datos que voy a pasarte debes generar una conclusión.

Este indicador estima si existe un volumen elevado de cambios de stock que pueda indicar irregularidades.

Analiza:

- Número de operaciones.
- Variación de unidades.
- Distribución por motivo.

Presta especial atención al motivo "Stock Manual". Los cambios elevados asociados a "Devolución Venta" pueden ser normales.

Analiza también la evolución temporal.

Incluye el porcentaje que representa cada usuario sobre el total de cambios de stock.

Utiliza únicamente los datos del apartado "TEXTO CON LOS DATOS PARA REDACTAR LA CONCLUSIÓN".

No uses la expresión "En conclusión".

Añade un pequeño comentario sobre el último mes.

Usa comas para los decimales y puntos para los miles.

Si aparece el usuario -1, sustitúyelo por "usuario administrador".

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

TEXTO CON LOS DATOS PARA REDACTAR LA CONCLUSIÓN:



"""
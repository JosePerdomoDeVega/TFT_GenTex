cp_prompt = """
Usando los datos que voy a pasarte debes generar una conclusión.

Este indicador estima si en una OF se están realizando muchas devoluciones usando como código de producto un código que no corresponda con un producto de venta en la farmacia, como promociones, bolsas, servicios, etc. Al no modificar el stock en muchos casos, estos códigos pueden usarse para cometer movimientos fraudulentos.

Las cifras que deben analizarse, junto con su distribución por usuario y mes, son las siguientes:

- Número de unidades devueltas de productos con códigos propios
- Distribución del número de unidades devueltas por códigos propios más destacados
- Importe neto total de las devoluciones con códigos propios
- Precio medio de las devoluciones con códigos propios
- Ratio de devoluciones con códigos propios

Para una mayor seguridad y control de las operaciones, es recomendable no reutilizar códigos (es decir, que cada código propio de la farmacia se utilice para un único concepto).

Se debe analizar la evolución a lo largo del tiempo con el fin de identificar tendencias o patrones.

ASEGÚRATE DE USAR EXACTAMENTE LOS DATOS DEL APARTADO "TEXTO CON LOS DATOS PARA REDACTAR LA CONCLUSIÓN".

No uses la expresión "En conclusión".

Añade un pequeño párrafo sobre la evolución del indicador en el último mes.

Usa comas para los decimales y puntos para los miles.

Si aparece el usuario -1, cambia su nombre por "usuario administrador".

Cuando menciones un código de producto, utiliza su descripción.

TEXTO CON LOS DATOS PARA REDACTAR LA CONCLUSIÓN:

"""
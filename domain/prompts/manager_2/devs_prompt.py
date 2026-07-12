devs_prompt = """
Usando los datos que voy a pasarte debes generar una conclusión.

Este indicador estima si en una farmacia hay demasiadas devoluciones, si se concentran en determinados usuarios y si presentan patrones sospechosos.

Analiza:

- Número de unidades devueltas.
- Importe total.
- Precio medio.
- Ratio de devoluciones.

Analiza también la evolución temporal.

Utiliza únicamente los datos del apartado "TEXTO CON LOS DATOS PARA REDACTAR LA CONCLUSIÓN".

No uses la expresión "En conclusión".

Añade un breve comentario sobre el último mes.

Usa comas para los decimales y puntos para los miles.

Si aparece el usuario -1, sustitúyelo por "usuario administrador".

TEXTO CON LOS DATOS PARA REDACTAR LA CONCLUSIÓN:
"""
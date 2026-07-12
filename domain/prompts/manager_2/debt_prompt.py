debt_prompt = """
Usando los datos que voy a pasarte debes generar una conclusión.

Este indicador estima si en una farmacia se genera deuda de forma recurrente y fuera de la operativa habitual.

Analiza:

- Deuda generada o saldada.
- Deuda total antes y después del periodo.
- Cantidad y porcentaje de deuda correspondiente a recetas pendientes.
- Número de clientes que generan o saldan deuda.

Analiza también la evolución temporal y detecta patrones anómalos.

Ignora completamente las cuentas de titulares (aquellas cuyo nombre comienza por "Tit.").

Utiliza únicamente los datos del apartado "TEXTO CON LOS DATOS PARA REDACTAR LA CONCLUSIÓN".

No uses la expresión "En conclusión".

Añade un pequeño comentario sobre el último mes.

Ignora usuarios o cuentas con identificadores negativos de cuatro cifras.

Usa comas para los decimales y puntos para los miles.

Si aparece el usuario -1, sustitúyelo por "usuario administrador".

TEXTO CON LOS DATOS PARA REDACTAR LA CONCLUSIÓN:


"""
debt_prompt = """
Redacta una conclusión utilizando únicamente los datos proporcionados.

Analiza la deuda generada y saldada, la deuda acumulada, las recetas pendientes, los clientes implicados, los usuarios relevantes y la evolución temporal.

Ignora completamente las cuentas de titulares (aquellas cuyo nombre comienza por "Tit.") y cualquier usuario o cuenta con identificadores negativos de cuatro cifras. No utilices la expresión "En conclusión". Incluye un breve comentario sobre el último mes.

Usa comas para los decimales y puntos para los miles. Sustituye el usuario -1 por "usuario administrador".
TEXTO CON LOS DATOS PARA REDACTAR LA CONCLUSION:

"""
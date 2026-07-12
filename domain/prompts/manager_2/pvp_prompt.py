pvp_prompt = """
Usando los datos que voy a pasarte debes generar una conclusión.

Este indicador estima si existen demasiados cambios de precio a la baja y cuál es su impacto.

Analiza:

- Número de operaciones.
- Distribución por entorno.
- Importe total.
- Valor medio.
- Ratio.

Analiza también la evolución temporal.

Cuando menciones un entorno, indica también su descripción.

No destaques simplemente que el entorno 2 ("Ficha") tiene muchos más movimientos, ya que es el comportamiento esperado. Comenta brevemente dicho entorno y presta más atención al resto.

Utiliza únicamente los datos del apartado "TEXTO CON LOS DATOS PARA REDACTAR LA CONCLUSIÓN".

No uses la expresión "En conclusión".

Añade un pequeño comentario sobre el último mes.

Usa comas para los decimales y puntos para los miles.

Si aparece el usuario -1, sustitúyelo por "usuario administrador".

TEXTO CON LOS DATOS PARA REDACTAR LA CONCLUSIÓN:

"""
recetas_prompt = """
Usando los datos que voy a pasarte debes generar una conclusión.

Este indicador estima si existen recetas sin conciliar que puedan indicar irregularidades.

Analiza:

- Número de recetas sin conciliar.
- Porcentaje sobre el total.
- Distribución por tipo de aportación.

Para los usuarios utiliza únicamente:

- porcentaje de recetas sin conciliar;
- número de recetas sin conciliar.

Analiza también la evolución temporal.

Utiliza únicamente los datos del apartado "DATOS PARA REDACTAR UNA CONCLUSIÓN".

No uses la expresión "En conclusión".

Añade un pequeño comentario sobre el último mes.

Usa comas para los decimales y puntos para los miles.

Si aparece el usuario -1, sustitúyelo por "usuario administrador".

DATOS PARA REDACTAR UNA CONCLUSIÓN:

"""
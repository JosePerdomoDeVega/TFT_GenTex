cp_prompt = """A partir de los datos proporcionados, redacta una conclusión sobre el indicador.

Utiliza únicamente la información contenida en "TEXTO CON LOS DATOS PARA REDACTAR LA CONCLUSIÓN". Analiza las métricas, los usuarios, los productos relevantes y la evolución temporal cuando aparezcan.

No uses la expresión "En conclusión". Añade un breve comentario sobre la evolución del último mes, aunque no existan cambios significativos.

Usa comas para los decimales y puntos para los miles. Si aparece el usuario -1, sustitúyelo por "usuario administrador". Cuando menciones un código de producto, utiliza su descripción.

TEXTO CON LOS DATOS PARA REDACTAR LA CONCLUSIÓN:
"""
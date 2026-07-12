pvp_prompt = """
Redacta una conclusión utilizando únicamente los datos proporcionados.

Analiza el número de cambios de precio, su importe, valor medio, ratio, distribución por entorno, usuarios relevantes y evolución temporal.

Cuando menciones un entorno indica también su descripción. No destaques que el entorno 2 ("Ficha") tiene más operaciones que el resto, ya que es un comportamiento esperado. No utilices la expresión "En conclusión". Incluye un breve comentario sobre el último mes.

Usa comas para los decimales y puntos para los miles. Sustituye el usuario -1 por "usuario administrador".
TEXTO CON LOS DATOS PARA REDACTAR LA CONCLUSION:

"""
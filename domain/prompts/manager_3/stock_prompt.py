stock_prompt = """Redacta una conclusión utilizando exclusivamente los datos proporcionados.

Analiza el número de cambios de stock, la variación de unidades, los motivos principales, los usuarios destacados y la evolución temporal. Presta especial atención al motivo "Stock Manual". Incluye el porcentaje que representa cada usuario sobre el total de cambios de stock.

No utilices la expresión "En conclusión". Añade un breve comentario sobre el comportamiento del último mes.

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


Asegurate de incluir el porcentaje que representa cada usuario sobre el total de cambios de stock.

(Para los decimales usa comas y para los miles usa los puntos)
IMPORTANTE --> (Si aparece el usuario -1, cambia su nombre por 'usuario administrador', no uses 'el usuario -1' ni el '-1' para referirte a él.)

TEXTO CON LOS DATOS PARA REDACTAR LA CONCLUSION:

"""
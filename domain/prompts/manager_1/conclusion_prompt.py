conclusion_prompt = """
Quiero que actúes como un sintetizador de información. Te voy a proporcionar seis textos diferentes, cada uno es un indicador sobre el estado de una farmacia. Tu tarea será generar un texto final de seis párrafos, donde cada párrafo sea un breve resumen del texto correspondiente.

Instrucciones específicas:

Un párrafo por texto: el primer párrafo resume el primer texto, el segundo párrafo el segundo texto, y así sucesivamente.

Cada párrafo debe ser breve.

Incluye conclusiones globales pero no mezcles la información entre párrafos.

Mantén el orden original de los textos.

No repitas frases textuales, reescribe todo con tus propias palabras.

Cuando termines, entrega únicamente el texto final con sus seis párrafos.


TEXTOS:


"""
# GenTex — Generación automática de informes de farmacias

GenTex es un sistema que genera de forma automática los informes mensuales de
farmacias a partir de datos estructurados. Extrae los indicadores de negocio de
una base de datos relacional, los transforma y, mediante un modelo de lenguaje
(Azure OpenAI) y estrategias de prompting, redacta un texto por indicador y una
conclusión global. Una interfaz web permite a la persona experta revisar, editar
y validar el contenido antes de aprobarlo (flujo human-in-the-loop).

Este repositorio acompaña al Trabajo de Fin de Título del Grado en Ciencia e
Ingeniería de Datos (ULPGC).

## Arquitectura

El proyecto sigue una arquitectura hexagonal (puertos y adaptadores) organizada
en tres capas:

- `domain/`: núcleo de negocio, sin dependencias de infraestructura. Modelos,
  configuración, puertos (interfaces), plantillas de prompts y funciones de
  extracción y transformación por indicador.
- `services/`: adaptadores que implementan los puertos. Repositorio sobre SQL
  Server y agente de generación sobre Azure OpenAI.
- `applications/`: capa de entrada. Orquestación de casos de uso, API REST,
  interfaz web e inyección de dependencias.

Las dependencias apuntan siempre hacia el dominio.

## Requisitos previos

- Python 3.11 o superior.
- Controlador ODBC para SQL Server instalado en el sistema.
- Acceso a una base de datos SQL Server / Azure SQL.
- Un recurso de Azure OpenAI con un despliegue de modelo disponible.
- Docker (opcional, para el despliegue en contenedor).

## Instalación

```bash
git clone https://github.com/JosePerdomoDeVega/TFT_GenTex.git
cd TFT_GenTex

python -m venv .venv
source .venv/bin/activate        # En Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

## Configuración

La configuración se realiza mediante variables de entorno. Copia la plantilla y
rellena tus valores:

```bash
cp .env.example .env
```

Variables disponibles:

| Variable                     | Descripción                                        |
|------------------------------|----------------------------------------------------|
| `DB_SERVER`                  | Host del servidor de base de datos.                |
| `DB_NAME`                    | Nombre de la base de datos.                        |
| `DB_USER`                    | Usuario de base de datos.                          |
| `DB_PASSWORD`                | Contraseña de base de datos.                       |
| `AZURE_OPENAI_ENDPOINT`      | Endpoint del recurso de Azure OpenAI.              |
| `AZURE_OPENAI_API_KEY`       | Clave de API del servicio.                         |
| `AZURE_OPENAI_DEPLOYMENT`    | Nombre del despliegue del modelo.                  |
| `AZURE_OPENAI_API_VERSION`   | Versión de la API de Azure OpenAI.                 |

Los secretos se gestionan solo a través de este fichero y nunca se incluyen en el
código. El fichero `.env` no debe subirse al repositorio.

## Ejecución local

```bash
uvicorn main:app --reload
```

La aplicación queda disponible en `http://localhost:8000/conclusions`.

## Despliegue con Docker

```bash
# Construir la imagen
docker build -t gentex .

# Ejecutar el contenedor cargando las variables de entorno
docker run --env-file .env -p 8000:8000 gentex
```

## Uso

El flujo de trabajo desde la interfaz web es el siguiente:

1. Acceder a `/conclusions` desde el navegador.
2. Introducir el identificador del análisis mensual (`ax_id`, que asocia una
   farmacia con su análisis de un mes) y, opcionalmente, seleccionar los
   indicadores a incluir. Sin selección se usan todos por defecto.
3. Lanzar la generación. El sistema extrae los datos, genera un texto por
   indicador y una conclusión global, y los muestra en campos editables.
4. Revisar cada bloque, editarlo si es necesario y validar el informe, que queda
   persistido.

## API REST

| Método | Ruta                              | Descripción                                   |
|--------|-----------------------------------|-----------------------------------------------|
| GET    | `/health`                         | Comprobación del estado del servicio.         |
| GET    | `/conclusions`                    | Sirve la interfaz de usuario (HTML).          |
| POST   | `/conclusions`                    | Lanza la generación de un informe.            |
| GET    | `/applications/ui/{filename}`     | Sirve recursos estáticos (protegido).         |
| GET    | `/favicon.ico`                    | Icono de la aplicación.                       |

Ejemplo de petición a `POST /conclusions`:

```json
{
  "ax_id": 1234,
  "indicators": ["devoluciones", "deuda", "stock"]
}
```

Ejemplo de respuesta:

```json
{
  "ax_id": 1234,
  "reports": [
    {
      "indicator": "devoluciones",
      "text": "Durante el periodo analizado, las devoluciones..."
    },
    {
      "indicator": "deuda",
      "text": "La deuda acumulada muestra una variacion..."
    }
  ],
  "conclusion": "En conjunto, la farmacia presenta..."
}
```

Si el campo `indicators` se envía vacío, se emplea el conjunto por defecto
(`DEFAULT_INDICATORS`), con los seis indicadores soportados: devoluciones, deuda,
codigos_propios, pvp, recetas y stock.

## Pruebas

Las pruebas se ejecutan con pytest. La inyección de dependencias permite
sustituir el repositorio y el agente reales por dobles de prueba, de modo que se
verifica el caso de uso sin acceder a la base de datos ni al servicio de
generación.

```bash
pytest
```

| Qué se prueba                          | Cómo se prueba                                             | Resultado esperado                          |
|----------------------------------------|-----------------------------------------------------------|---------------------------------------------|
| Endpoint `POST /conclusions`           | `TestClient` con repositorio y agente simulados (mocks).  | Código 200 y respuesta con la estructura `ConclusionResponse`. |
| Orquestación de `ConclusionService`    | Doble de prueba del agente que devuelve texto fijo.       | Se genera un informe por indicador solicitado. |
| Selección por defecto de indicadores   | Petición con `indicators` vacío.                          | Se usan los seis indicadores por defecto.   |
| Aislamiento de dependencias externas   | Sobrescritura de proveedores con `dependency_overrides`.  | No se realizan llamadas reales a BD ni a Azure OpenAI. |

## Estructura del repositorio
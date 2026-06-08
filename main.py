from fastapi import FastAPI
from applications.api_routers import api_router

app = FastAPI(title="Automatización de Análisis de Textos de Farmacias")

app.include_router(api_router)

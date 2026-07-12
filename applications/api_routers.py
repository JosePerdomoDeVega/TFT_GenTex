from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from applications.conclusion import ConclusionService
from applications.dependencies import get_pharmacy_repository, get_text_agent
from domain.interfaces import PharmacyRepository, TextGenerationAgent
from domain.models import ConclusionRequest, ConclusionResponse, ValidationRequest

UI_DIR = Path(__file__).parent / "ui"
_STATIC_MEDIA_TYPES = {".css": "text/css", ".js": "application/javascript", ".svg": "image/svg+xml"}

api_router = APIRouter()


@api_router.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    return {"status": "ok"}


@api_router.get("/favicon.ico", include_in_schema=False)
async def favicon() -> FileResponse:
    return FileResponse(UI_DIR / "favicon.ico", media_type="image/svg+xml")


@api_router.get("/conclusions", include_in_schema=False)
async def conclusions_ui() -> FileResponse:
    return FileResponse(UI_DIR / "index.html", media_type="text/html")


@api_router.get("/applications/ui/{filename}", include_in_schema=False)
async def ui_static(filename: str) -> FileResponse:
    file_path = (UI_DIR / filename).resolve()

    if UI_DIR.resolve() not in file_path.parents or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Recurso no encontrado")
    media_type = _STATIC_MEDIA_TYPES.get(file_path.suffix, "application/octet-stream")

    return FileResponse(file_path, media_type=media_type)


@api_router.post("/conclusions", response_model=ConclusionResponse, tags=["conclusions"])
async def generate_conclusion(request: ConclusionRequest, repository: PharmacyRepository = Depends(get_pharmacy_repository), agent: TextGenerationAgent = Depends(get_text_agent)) -> ConclusionResponse:

    service = ConclusionService(repository, agent)
    return await service.generate(request)


@api_router.post("/conclusions/validate", tags=["conclusions"])
async def validate_conclusion(request: ValidationRequest, repository: PharmacyRepository = Depends(get_pharmacy_repository), agent: TextGenerationAgent = Depends(get_text_agent)) -> dict[str, str]:

    service = ConclusionService(repository, agent)
    service.validate(request)
    return {"status": "saved", "ax_id": request.ax_id}

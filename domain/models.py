from datetime import datetime
from enum import Enum
from typing import Any
from pydantic import BaseModel, Field


class Indicator(str, Enum):

    devoluciones = "devoluciones"
    deuda = "deuda"
    codigos_propios = "codigos_propios"
    pvp = "pvp"
    recetas = "recetas"
    stock = "stock"


class AnalysisPeriod(BaseModel):

    start: datetime
    end: datetime


class IndicatorData(BaseModel):

    ax_id: str
    indicator: Indicator
    data: Any


class IndicatorReport(BaseModel):

    indicator: Indicator
    text: str


class ConclusionRequest(BaseModel):

    ax_id: str = Field(..., examples=["OF00053_2"])
    indicators: list[Indicator] = Field(default_factory=lambda: list(DEFAULT_INDICATORS))


class ConclusionResponse(BaseModel):

    ax_id: str
    reports: list[IndicatorReport]
    conclusion: str


class ValidationRequest(BaseModel):

    ax_id: str
    reports: list[IndicatorReport]
    conclusion: str


DEFAULT_INDICATORS: tuple[Indicator, ...] = (
    Indicator.devoluciones, Indicator.deuda, Indicator.codigos_propios,
    Indicator.pvp, Indicator.recetas, Indicator.stock,
)

from typing import Any
import pandas as pd


def filter_stock(df: pd.DataFrame, ax_id: str, start, end) -> dict[str, Any]:
    df = df.copy()
    df["fecha"] = pd.to_datetime(df["fecha"])
    filtered_df = df[(df["ax_id"] == ax_id) & (df["fecha"] >= start) & (df["fecha"] <= end)].copy()
    filtered_df["year_month"] = filtered_df["fecha"].dt.to_period("M")

    var_per_month = filtered_df.groupby("year_month")["variacion_unidades"].sum()
    total_variacion_unidades = filtered_df["variacion_unidades"].sum()
    total_operaciones = filtered_df["count_operaciones"].sum()

    usuario_counts = filtered_df["usuario"].value_counts()
    usuario_percentages = usuario_counts / usuario_counts.sum() * 100 if usuario_counts.sum() else usuario_counts * 0.0
    motivo_counts = filtered_df["motivo"].value_counts()
    motivo_percentages = motivo_counts / motivo_counts.sum() * 100 if motivo_counts.sum() else motivo_counts * 0.0

    return {
        "Variación total de unidades de stock": total_variacion_unidades,
        "Número total de operaciones de cambio de stock": total_operaciones,
        "Porcentaje de cambios de stock por usuario": usuario_percentages.to_dict(),
        "Motivos más comunes de cambio de stock y sus porcentajes": motivo_percentages.to_dict(),
        "Evaluacion por mes: ": var_per_month,
    }

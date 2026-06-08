import pandas as pd


def filter_conciliacion(df: pd.DataFrame, ax_id: str, start, end) -> str:
    df = df.copy()
    df["fecha"] = pd.to_datetime(df["fecha"])
    filtered_df = df[(df["of_id"] == ax_id[0:-2]) & (df["ax_id"] == ax_id) & (df["fecha"] >= start) & (df["fecha"] <= end)].copy()
    filtered_df["year_month"] = filtered_df["fecha"].dt.to_period("M")

    total_recetas = filtered_df["count_total"].sum()
    recetas_sin_conciliar = filtered_df["count_sin_conciliar2"].sum()
    var_per_month = filtered_df.groupby("year_month")["count_sin_conciliar2"].sum()
    porcentaje_conciliadas = (total_recetas - recetas_sin_conciliar) / total_recetas * 100
    porcentaje_no_conciliadas = recetas_sin_conciliar / total_recetas * 100

    recetas_por_usuario = filtered_df.groupby("usuario")[["count_total", "count_sin_conciliar2"]].sum()
    recetas_por_usuario.reset_index(drop=True, inplace=True)
    recetas_por_usuario["porcentaje_sin_conciliar"] = (
        recetas_por_usuario["count_sin_conciliar2"].values
        / recetas_por_usuario["count_total"].values
    ) * 100
    recetas_por_usuario = recetas_por_usuario.drop(columns=["count_total"])

    return (
        f"Número total de recetas: {total_recetas}\n"
        f"Número de recetas sin conciliar: {recetas_sin_conciliar}\n"
        f"Porcentaje de recetas conciliadas: {porcentaje_conciliadas:.2f}%\n"
        f"Porcentaje de recetas no conciliadas: {porcentaje_no_conciliadas:.2f}%\n\n"
        f"Variación por mes: {var_per_month}\n\n"
        "Recetas sin conciliar por usuario:\n"
        f"{recetas_por_usuario.to_string()}"
    )

import pandas as pd
import pyodbc


def get_devs(conn: pyodbc.Connection, ax_id: str) -> pd.DataFrame:
    query = "SELECT * FROM v_estadisticas_usuarios WHERE ax_id LIKE ?"
    return pd.read_sql(query, conn, params=[ax_id])


def filter_devs(df: pd.DataFrame, ax_id: str, start, end, devs: pd.DataFrame) -> str:
    df = df.copy()
    df["fecha"] = pd.to_datetime(df["fecha"])
    filtered_df = df[(df["ax_id"] == ax_id) & (df["fecha"] >= start) & (df["fecha"] <= end)].copy()
    filtered_df["year_month"] = filtered_df["fecha"].dt.to_period("M")
    filtered_df["importe_bruto_abs"] = filtered_df["importe_neto"].abs()
    filtered_df["unidades_abs"] = filtered_df["unidades"].abs()

    total_importe_devoluciones = filtered_df["importe_bruto_abs"].sum()
    total_unidades_devueltas = filtered_df["unidades_abs"].sum()
    precio_medio_devolucion = total_importe_devoluciones / total_unidades_devueltas

    precio_medio_devolucion_usuario = filtered_df[["usuario", "importe_neto", "unidades"]].groupby("usuario").sum()
    precio_medio_devolucion_usuario["precio_medio_dev"] = (
        precio_medio_devolucion_usuario["importe_neto"] / precio_medio_devolucion_usuario["unidades"]
    )
    precio_medio_devolucion_usuario["unidades"] = -precio_medio_devolucion_usuario["unidades"]
    precio_medio_devolucion_usuario["importe_neto"] = -precio_medio_devolucion_usuario["importe_neto"]

    top_usuarios_unidades = filtered_df.groupby("usuario")["unidades_abs"].sum().nlargest(3)
    filtered_df["precio_medio_usuario"] = filtered_df["importe_bruto_abs"] / filtered_df["unidades_abs"]

    total_devs = devs["count_lineas_devs"].sum()
    total_purchases = devs["count_lineas"].sum()
    ratio_medio_devoluciones = round((total_devs / total_purchases) * 100, 2)

    top_usuarios_ratio = devs[["usuario", "count_lineas", "count_lineas_devs"]].groupby("usuario").sum()
    top_usuarios_ratio["ratio_devs"] = (
        top_usuarios_ratio["count_lineas_devs"] / top_usuarios_ratio["count_lineas"] * 100
    )

    evolucion_mensual_importe = filtered_df.groupby("year_month")["importe_bruto_abs"].sum()
    cambios_significativos_usuario = (
        filtered_df.groupby(["usuario", "year_month"])["importe_bruto_abs"]
        .sum()
        .unstack()
        .fillna(0)
        .diff(axis=1)
    )

    return f"""
        Número total de unidades devueltas: {total_unidades_devueltas:.0f}
        Importe total de devoluciones (€): {total_importe_devoluciones:.2f}
        Precio medio de devolución (€): {precio_medio_devolucion:.2f}
        Ratio medio de devoluciones: {ratio_medio_devoluciones:.4f}

        Usuarios con más unidades devueltas:
        {top_usuarios_unidades.to_string()}

        Precio medio por usuario:
        {precio_medio_devolucion_usuario}

        Evolución mensual del importe total de devoluciones (€):
        {evolucion_mensual_importe.to_string()}

        Cambios significativos por usuario en el tiempo (importe bruto):
        {cambios_significativos_usuario.to_string()}
        """

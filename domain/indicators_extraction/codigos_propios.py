import pandas as pd
import pyodbc


def get_devs_cp(conn: pyodbc.Connection, ax_id: str) -> pd.DataFrame:
    query = "SELECT * FROM v_estadisticas_usuarios WHERE ax_id LIKE ?"
    return pd.read_sql(query, conn, params=[ax_id])


def get_df_desc(conn: pyodbc.Connection, ax_id: str) -> pd.DataFrame:
    query = "SELECT producto_codigo, producto_descripcion FROM dx_codigos_propios_detalle WHERE ix_id LIKE ?"
    return pd.read_sql(query, conn, params=[f"{ax_id}%"])


def filter_devs_cp(df: pd.DataFrame, ax_id: str, start, end, devs: pd.DataFrame, df_desc: pd.DataFrame) -> str:
    df = df.copy()
    df["fecha"] = pd.to_datetime(df["fecha"])
    filtered_df = df[(df["ax_id"] == ax_id) & (df["fecha"] >= start) & (df["fecha"] <= end)].copy()
    filtered_df["year_month"] = filtered_df["fecha"].dt.to_period("M")
    filtered_df["importe_bruto_abs"] = filtered_df["importe_bruto"].abs()
    filtered_df["unidades_abs"] = filtered_df["unidades"].abs()

    total_importe_devoluciones = filtered_df["importe_bruto_abs"].sum()
    total_unidades_devueltas = filtered_df["unidades_abs"].sum()

    if total_unidades_devueltas == 0:
        precio_medio_devolucion = 0.0
    else:
        precio_medio_devolucion = round(total_importe_devoluciones / total_unidades_devueltas, 2)

    precio_medio_devolucion_usuario = filtered_df[["usuario", "importe_neto", "unidades"]].groupby("usuario").sum()
    precio_medio_devolucion_usuario["precio_medio_dev"] = precio_medio_devolucion_usuario["importe_neto"] / precio_medio_devolucion_usuario["unidades"]
    precio_medio_devolucion_usuario["unidades"] = -precio_medio_devolucion_usuario["unidades"]
    precio_medio_devolucion_usuario["importe_neto"] = -precio_medio_devolucion_usuario["importe_neto"]

    cols = ["importe_bruto_abs", "unidades_abs"]
    filtered_df[cols] = filtered_df[cols].apply(pd.to_numeric, errors="coerce")

    top_usuarios_unidades = filtered_df.groupby("usuario")["unidades_abs"].sum().astype(float).nlargest(3)

    filtered_df["precio_medio_usuario"] = filtered_df["importe_bruto_abs"] / filtered_df["unidades_abs"]

    total_devs = devs["count_lineas_devs_cp"].sum()
    total_purchases = devs["count_lineas"].sum()
    ratio_medio_devoluciones = round((total_devs / total_purchases) * 100, 2)

    top_usuarios_ratio = devs[["usuario", "count_lineas", "count_lineas_devs"]].groupby("usuario").sum()
    top_usuarios_ratio["ratio_devs"] = top_usuarios_ratio["count_lineas_devs"] / top_usuarios_ratio["count_lineas"] * 100

    evolucion_mensual_importe = filtered_df.groupby("year_month")["importe_bruto_abs"].sum()
    cambios_significativos_usuario = filtered_df.groupby(["usuario", "year_month"])["importe_bruto_abs"].sum().unstack().fillna(0).diff(axis=1)

    filtered_df["unidades"] = filtered_df["unidades"] * -1
    filtered_df["producto_codigo"] = filtered_df["codigo_producto"]

    sales = filtered_df[["unidades", "producto_codigo"]].groupby("producto_codigo").sum()
    df_desc = df_desc.groupby("producto_codigo").first()
    sales_desc = pd.merge(sales, df_desc, on="producto_codigo", how="inner")
    sales_desc["porcentaje"] = round((sales_desc["unidades"].astype(int) / sales_desc["unidades"].astype(int).sum()) * 100, 2)

    return f"""
        Número total de unidades devueltas: {total_unidades_devueltas:.0f}
        Importe total de devoluciones (€): {total_importe_devoluciones:.2f}
        Precio medio de devolución (€): {precio_medio_devolucion:.2f}
        Ratio medio de devoluciones: {ratio_medio_devoluciones:.2f}

        Usuarios con más unidades devueltas:
        {top_usuarios_unidades.to_string()}

        Precio medio por usuario:
        {precio_medio_devolucion_usuario}

        Evolución mensual del importe total de devoluciones (€):
        {evolucion_mensual_importe.to_string()}

        Cambios significativos por usuario en el tiempo (importe bruto):
        {cambios_significativos_usuario.to_string()}

        Códigos con más unidades con su descripcion: {sales_desc}
        """

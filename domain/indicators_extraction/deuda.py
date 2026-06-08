from typing import Any
import pandas as pd
import pyodbc


def get_total_deuda(conn: pyodbc.Connection, ax_id: str) -> float:
    query = "SELECT saldo_total FROM v_deuda_historico WHERE ax_id LIKE ?"
    return pd.read_sql(query, conn, params=[ax_id])["saldo_total"].sum()


def filter_deuda(df: pd.DataFrame, ax_id: str, start, end, total_deuda: float) -> dict[str, Any]:
    df = df.copy()
    df["fecha"] = pd.to_datetime(df["fecha"])
    filtered_df = df[(df["ax_id"] == ax_id) & (df["fecha"] >= start) & (df["fecha"] <= end)].copy()
    filtered_df["year_month"] = filtered_df["fecha"].dt.to_period("M")

    deuda_durante_el_periodo = filtered_df["variacion_deuda"].sum()
    var_per_month = filtered_df.groupby("year_month")["variacion_deuda"].sum()

    usuarios_deuda = filtered_df.groupby("usuario")["variacion_deuda"].agg(["sum", "count"]).reset_index()
    usuarios_deuda.columns = ["Usuario", "Deuda Generada", "Transacciones"]

    deuda_por_cuenta = filtered_df.groupby("cc_of")["variacion_deuda"].sum().reset_index()
    top_3 = deuda_por_cuenta.nlargest(3, "variacion_deuda")
    bottom_3 = deuda_por_cuenta.nsmallest(3, "variacion_deuda")
    deuda_por_cuenta_cliente = pd.concat([top_3, bottom_3])

    return {
        "Deuda en el Periodo": deuda_durante_el_periodo,
        "Usuarios y Deuda": usuarios_deuda,
        "Deuda por Cuenta de Cliente": deuda_por_cuenta_cliente,
        "Deuda Total Acumulada": total_deuda,
        "Deuda por Meses: ": var_per_month,
    }

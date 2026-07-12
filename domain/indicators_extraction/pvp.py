import pandas as pd
import pyodbc


def get_pvp_entornos(conn: pyodbc.Connection, ax_id: str) -> pd.DataFrame:
    query = "SELECT codigo, descripcion FROM v_leyenda_entornos_pvp WHERE ax_id LIKE ? AND codigo <> 2"
    entornos = pd.read_sql(query, conn, params=[f"{ax_id}%"])
    return entornos.rename(columns={"codigo": "entorno_id"})


def get_chg_pvp(conn: pyodbc.Connection, ax_id: str) -> pd.DataFrame:
    query = "SELECT usuario, count_lineas, count_lineas_chg_pvp FROM v_estadisticas_usuarios WHERE ax_id LIKE ?"
    return pd.read_sql(query, conn, params=[ax_id])


def filter_chg_pvp(df: pd.DataFrame, ax_id: str, start, end, chg_pvp: pd.DataFrame, entornos: pd.DataFrame) -> str:
    df = df.copy()
    df["fecha"] = pd.to_datetime(df["fecha"])
    filtered = df[(df["ax_id"] == ax_id) & (df["fecha"].between(start, end))].copy()
    filtered["year_month"] = filtered["fecha"].dt.to_period("M")

    total_price = filtered["dif_pvp"].sum()
    total_operations = filtered["count"].sum()
    average_price_change = total_price / total_operations if total_operations else 0

    users_operations = filtered.groupby("usuario")["count"].sum()
    user_mean_chg_price = filtered.groupby("usuario").apply(
        lambda g: g["dif_pvp"].sum() / g["count"].sum() if g["count"].sum() else 0
    )

    var_per_month = filtered.groupby("year_month")["dif_pvp"].sum()
    main_categories = filtered["categoria"].value_counts().head(3).index.tolist()

    total_lines_pvp = chg_pvp["count_lineas_chg_pvp"].sum()
    lines_diario = chg_pvp["count_lineas"].sum()
    ratio_medio_chg_pvp = round((total_lines_pvp / lines_diario) * 100, 2) if lines_diario else 0

    chg_entorno = filtered.groupby("entorno_id", as_index=False)["dif_pvp"].sum()
    cambios_precio_entorno = pd.merge(chg_entorno, entornos, on="entorno_id", how="right")

    return f"""
    Cifras generales del indicador:
    - Volumen total de operaciones: {total_operations}
    - Importe total de cambios de precio: {total_price}
    - Cambios de precio medio: {average_price_change}

    Datos destacados por usuarios:
    - Operaciones por usuarios: {users_operations}

    Conceptos o categorías principales que impactan los datos:
    - Principales categorías: {main_categories}

    Cambios de precio medio por usuario: {user_mean_chg_price}

    Ratio Global de movimientos de cambios de precio: {ratio_medio_chg_pvp}

    Valor y operaciones Totales de cambios de precio por entorno: {cambios_precio_entorno}

    Variación del indicador por meses: {var_per_month}
    """

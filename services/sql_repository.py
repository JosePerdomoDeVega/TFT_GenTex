import pandas as pd
from domain.interfaces import PharmacyRepository
from domain.models import AnalysisPeriod, Indicator, IndicatorData
from domain.settings import Settings
from domain.indicators_extraction.pvp import filter_chg_pvp, get_chg_pvp, get_pvp_entornos
from domain.indicators_extraction.codigos_propios import filter_devs_cp, get_devs_cp, get_df_desc
from domain.indicators_extraction.deuda import filter_deuda, get_total_deuda
from domain.indicators_extraction.devs import filter_devs, get_devs
from domain.indicators_extraction.stock import filter_stock
from domain.indicators_extraction.recetas import filter_conciliacion



QUERY_RECETAS = """
SELECT
    r.*,
    CASE
        WHEN EXISTS (
            SELECT 1
            FROM v_leyenda_aportaciones l
            WHERE l.ax_id = r.ax_id
              AND l.codigo = r.aportacion
              AND l.orden = 0
        )
        THEN r.count_sin_conciliar
        ELSE 0
    END AS count_sin_conciliar2
FROM v_recetas_agregado r
WHERE r.ax_id = ?;
"""

QUERIES: dict[Indicator, str] = {
    Indicator.devoluciones: "SELECT * FROM v_devoluciones_agregado WHERE ax_id LIKE ?",
    Indicator.pvp: "SELECT * FROM v_cambios_pvp_agregado WHERE ax_id = ? AND entorno_id <> 2",
    Indicator.recetas: QUERY_RECETAS,
    Indicator.codigos_propios: "SELECT * FROM v_codigos_propios_agregado WHERE ax_id = ?",
    Indicator.deuda: "SELECT * FROM v_deuda_agregado WHERE ax_id = ?",
    Indicator.stock: "SELECT * FROM v_stock_agregado WHERE ax_id = ? and motivo <> 22",
}


class SqlServerPharmacyRepository(PharmacyRepository):
    def __init__(self, settings: Settings):
        self._conn_str = settings.connection_string

    def _connect(self):
        import pyodbc

        return pyodbc.connect(self._conn_str)


    def get_analysis_period(self, ax_id: str) -> AnalysisPeriod:

        with self._connect() as conn:
            start = pd.read_sql("SELECT periodo_inicio FROM analisis WHERE ax_id LIKE ?", conn, params=[ax_id])["periodo_inicio"][0]
            end = pd.read_sql("SELECT periodo_fin FROM analisis WHERE ax_id LIKE ?", conn, params=[ax_id])["periodo_fin"][0]
            end = pd.Timestamp(end) + pd.offsets.MonthEnd(0)


        return AnalysisPeriod(start=pd.to_datetime(start), end=pd.to_datetime(end))


    def get_indicator_data(self, ax_id: str, indicator: Indicator, period: AnalysisPeriod) -> IndicatorData:

        with self._connect() as conn:
            df = pd.read_sql(QUERIES[indicator], conn, params=[ax_id])
            df["fecha"] = pd.to_datetime(df["fecha"])
            data = self._filter(conn, df, ax_id, indicator, period.start, period.end)

        return IndicatorData(ax_id=ax_id, indicator=indicator, data=data)

    @staticmethod
    def _filter(conn, df, ax_id, indicator: Indicator, start, end):
        if indicator == Indicator.devoluciones:
            return filter_devs(df, ax_id, start, end, get_devs(conn, ax_id))

        if indicator == Indicator.deuda:
            return filter_deuda(df, ax_id, start, end, get_total_deuda(conn, ax_id))

        if indicator == Indicator.codigos_propios:
            return filter_devs_cp(df, ax_id, start, end, get_devs_cp(conn, ax_id), get_df_desc(conn, ax_id))

        if indicator == Indicator.pvp:
            return filter_chg_pvp(df, ax_id, start, end, get_chg_pvp(conn, ax_id), get_pvp_entornos(conn, ax_id))

        if indicator == Indicator.recetas:
            return filter_conciliacion(df, ax_id, start, end)

        if indicator == Indicator.stock:
            return filter_stock(df, ax_id, start, end)

        raise ValueError(f"Indicador no soportado: {indicator}")

    def save_text(self, ax_id: str, indicator: str, text: str, ambito: str = "ANALISIS_IX"):
        select_ix = "SELECT TOP 1 ix_id FROM indicadores WHERE ix_id LIKE ? ORDER BY ix_id DESC"
        merge_sql = """
            MERGE INTO [dbo].[textos] AS target
            USING (VALUES (?, ?, ?)) AS source (ix_id, ambito, texto)
                ON target.ix_id = source.ix_id AND target.ambito = source.ambito
            WHEN MATCHED THEN
                UPDATE SET texto = source.texto
            WHEN NOT MATCHED THEN
                INSERT (ix_id, ambito, texto)
                VALUES (source.ix_id, source.ambito, source.texto);
        """

        with self._connect() as conn:
            ix_id = pd.read_sql(select_ix, conn, params=[f"{ax_id}-%-{indicator}"]).iloc[0]["ix_id"]
            cursor = conn.cursor()
            cursor.execute(merge_sql, (ix_id, ambito, text))
            conn.commit()

    def get_indicator_texts(self, ax_id: str) -> dict:
        query = """
            SELECT texto FROM textos
            WHERE ix_id = (
                SELECT TOP 1 ix_id FROM indicadores
                WHERE ix_id LIKE ? ORDER BY ix_id DESC
            ) AND ambito = 'ANALISIS_IX';
        """
        texts = {}

        with self._connect() as conn:
            for indicator in QUERIES:
                df = pd.read_sql(query, conn, params=[f"{ax_id}-%-{indicator.value}"])
                if not df.empty:
                    texts[indicator.value] = df['texto'][0]
        return texts

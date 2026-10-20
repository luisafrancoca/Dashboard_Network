"""Dashboard de Redes - Interfaz de usuario con Streamlit."""

from __future__ import annotations

from typing import Final

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.alerts import THRESHOLDS, get_active_alerts
from utils.metrics import (
    get_device_status,
    get_metrics_by_region,
    get_summary_metrics,
    load_data,
)

PAGE_TITLE: Final[str] = "Dashboard de Redes"
DATA_PATH: Final[str] = "data/network_metrics.csv"

CSS: Final[str] = """
<style>
.metric-card {
    background: #1e1e1e;
    border: 1px solid #333;
    border-radius: 8px;
    padding: 1rem;
    text-align: center;
}
.metric-value {
    font-size: 1.5rem;
    font-weight: bold;
    color: #00D4FF;
}
.metric-label {
    font-size: 0.85rem;
    color: #aaa;
    margin-top: 0.25rem;
}
.alert-card {
    background: #2a1a1a;
    border: 1px solid #FF4B4B;
    border-radius: 8px;
    padding: 0.75rem;
    margin-bottom: 0.5rem;
}
.alert-crit {
    color: #FF4B4B;
    font-weight: bold;
}
.alert-warn {
    color: #FFA500;
    font-weight: bold;
}
</style>
"""


def inject_css() -> None:
    """Inyecta CSS personalizado (dark mode, tarjetas de alerta)."""
    st.markdown(CSS, unsafe_allow_html=True)


def load_csv_data(filepath: str) -> pd.DataFrame | None:
    """Carga el CSV mostrando error amigable si falla."""
    try:
        return load_data(filepath)
    except FileNotFoundError:
        st.error(f"No se encontró el archivo de datos: {filepath}")
        return None
    except ValueError as exc:
        st.error(f"Error de validación del CSV: {exc}")
        return None


def render_sidebar(df: pd.DataFrame) -> pd.DataFrame:
    """Sidebar con 3 filtros dinámicos y retorna el DataFrame filtrado."""
    st.sidebar.title("Filtros")

    regions = ["Todos"] + sorted(df["region"].dropna().unique().tolist())
    region = st.sidebar.selectbox("Región", regions)

    devices = ["Todos"] + sorted(df["device_id"].dropna().unique().tolist())
    device = st.sidebar.selectbox("Dispositivo", devices)

    statuses = ["Todos"] + sorted(df["status"].dropna().unique().tolist())
    status = st.sidebar.selectbox("Estado", statuses)

    filtered = df.copy()
    if region != "Todos":
        filtered = filtered[filtered["region"] == region]
    if device != "Todos":
        filtered = filtered[filtered["device_id"] == device]
    if status != "Todos":
        filtered = filtered[filtered["status"] == status]

    return filtered


def render_kpis(df: pd.DataFrame) -> None:
    """Renderiza las 5 columnas de KPIs."""
    metrics = get_summary_metrics(df)

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.markdown(
            f"<div class='metric-card'>"
            f"<div class='metric-value'>{metrics['total_devices']}</div>"
            f"<div class='metric-label'>Dispositivos</div>"
            f"</div>",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"<div class='metric-card'>"
            f"<div class='metric-value'>{metrics['avg_latency']:.1f}</div>"
            f"<div class='metric-label'>Latencia media (ms)</div>"
            f"</div>",
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"<div class='metric-card'>"
            f"<div class='metric-value'>{metrics['critical_count']}</div>"
            f"<div class='metric-label'>Críticos</div>"
            f"</div>",
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            f"<div class='metric-card'>"
            f"<div class='metric-value'>{metrics['avg_bandwidth_mbps']:.0f}</div>"
            f"<div class='metric-label'>Ancho de banda medio (Mbps)</div>"
            f"</div>",
            unsafe_allow_html=True,
        )
    with c5:
        st.markdown(
            f"<div class='metric-card'>"
            f"<div class='metric-value'>{metrics['avg_packet_loss_pct']:.2f}</div>"
            f"<div class='metric-label'>Pérdida de paquetes media (%)</div>"
            f"</div>",
            unsafe_allow_html=True,
        )


def render_alerts(df: pd.DataFrame) -> None:
    """Renderiza la sección de alertas activas."""
    st.subheader("🚨 Alertas Activas")
    alerts_df = get_active_alerts(df)

    if alerts_df.empty:
        st.info("No hay alertas activas.")
        return

    for _, row in alerts_df.iterrows():
        alert_html = "<div class='alert-card'>"
        alert_html += (
            f"<strong>{row.get('device_id', 'N/A')}</strong> "
            f"({row.get('device_name', 'N/A')}) - {row.get('region', 'N/A')}<br>"
        )
        for alert in row["alertas"]:
            cls = "alert-crit" if "CRÍTICO" in alert else "alert-warn"
            alert_html += f"<span class='{cls}'>{alert}</span><br>"
        alert_html += "</div>"
        st.markdown(alert_html, unsafe_allow_html=True)


def render_charts(df: pd.DataFrame) -> None:
    """Renderiza los 4 gráficos con Plotly Express."""
    st.subheader("📊 Gráficos")

    col1, col2 = st.columns(2)

    with col1:
        fig_latency = px.line(
            df.sort_values("timestamp"),
            x="timestamp",
            y="latency_ms",
            color="device_id",
            title="Latencia por dispositivo",
        )
        fig_latency.update_layout(template="plotly_dark")
        st.plotly_chart(fig_latency, use_container_width=True)

    with col2:
        fig_cpu = px.bar(
            df.groupby("device_id", as_index=False)["cpu_usage_pct"].mean(),
            x="device_id",
            y="cpu_usage_pct",
            title="Uso de CPU medio por dispositivo",
        )
        fig_cpu.update_layout(template="plotly_dark")
        st.plotly_chart(fig_cpu, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        fig_bw = px.line(
            df.sort_values("timestamp"),
            x="timestamp",
            y="bandwidth_mbps",
            color="device_id",
            title="Ancho de banda por dispositivo",
        )
        fig_bw.update_layout(template="plotly_dark")
        st.plotly_chart(fig_bw, use_container_width=True)

    with col4:
        region_metrics = get_metrics_by_region(df)
        fig_region = px.bar(
            region_metrics,
            x="region",
            y="latency_ms",
            title="Latencia media por región",
        )
        fig_region.update_layout(template="plotly_dark")
        st.plotly_chart(fig_region, use_container_width=True)


def render_table(df: pd.DataFrame) -> None:
    """Renderiza la tabla de dispositivos con st.dataframe y column_config."""
    st.subheader("📋 Tabla de Dispositivos")

    status_df = get_device_status(df)
    if status_df.empty:
        st.info("No hay datos para mostrar en la tabla.")
        return

    display_cols = [
        "timestamp",
        "device_id",
        "device_name",
        "region",
        "latency_ms",
        "bandwidth_mbps",
        "packet_loss_pct",
        "cpu_usage_pct",
        "memory_usage_pct",
        "status",
    ]
    display_cols = [c for c in display_cols if c in status_df.columns]

    st.dataframe(
        status_df[display_cols],
        use_container_width=True,
        column_config={
            "timestamp": st.column_config.DatetimeColumn("Fecha/Hora"),
            "device_id": st.column_config.TextColumn("ID Dispositivo"),
            "device_name": st.column_config.TextColumn("Nombre"),
            "region": st.column_config.TextColumn("Región"),
            "latency_ms": st.column_config.NumberColumn("Latencia (ms)", format="%.1f"),
            "bandwidth_mbps": st.column_config.NumberColumn(
                "Ancho de banda (Mbps)", format="%.0f"
            ),
            "packet_loss_pct": st.column_config.NumberColumn(
                "Pérdida paquetes (%)", format="%.2f"
            ),
            "cpu_usage_pct": st.column_config.NumberColumn("CPU (%)", format="%.0f"),
            "memory_usage_pct": st.column_config.NumberColumn("Memoria (%)", format="%.0f"),
            "status": st.column_config.TextColumn("Estado"),
        },
        hide_index=True,
    )


def render_downloads(df: pd.DataFrame) -> None:
    """Renderiza botones de descarga CSV."""
    st.subheader("⬇️ Descargas")

    col1, col2 = st.columns(2)

    with col1:
        csv_filtered = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Descargar datos filtrados (CSV)",
            data=csv_filtered,
            file_name="datos_filtrados.csv",
            mime="text/csv",
        )

    with col2:
        region_metrics = get_metrics_by_region(df)
        csv_region = region_metrics.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Descargar resumen por región (CSV)",
            data=csv_region,
            file_name="resumen_region.csv",
            mime="text/csv",
        )


def main() -> None:
    """Punto de entrada principal de la aplicación Streamlit."""
    st.set_page_config(
        page_title=PAGE_TITLE,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    inject_css()

    st.title("📶 Dashboard de Redes")

    df = load_csv_data(DATA_PATH)
    if df is None:
        st.stop()

    filtered_df = render_sidebar(df)

    render_kpis(filtered_df)
    st.divider()

    render_alerts(filtered_df)
    st.divider()

    render_charts(filtered_df)
    st.divider()

    render_table(filtered_df)
    st.divider()

    render_downloads(filtered_df)


if __name__ == "__main__":
    main()

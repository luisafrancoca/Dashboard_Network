"""Funciones de carga, limpieza y cálculo de KPIs para el dashboard de redes."""

from __future__ import annotations

from typing import Final

import pandas as pd

REQUIRED_COLUMNS: Final[list[str]] = [
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


def load_data(filepath: str) -> pd.DataFrame:
    """Carga y valida el CSV de métricas de red.

    Args:
        filepath: Ruta al archivo CSV.

    Returns:
        DataFrame con la columna 'timestamp' parseada como datetime.

    Raises:
        FileNotFoundError: Si el archivo no existe.
        ValueError: Si faltan columnas requeridas.
    """
    import os

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No se encontró el archivo: {filepath}")

    df = pd.read_csv(filepath)

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Columnas requeridas faltantes: {missing}")

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    return df


def get_summary_metrics(df: pd.DataFrame) -> dict:
    """Calcula los 5 KPIs resumen del DataFrame.

    Args:
        df: DataFrame de métricas de red.

    Returns:
        Diccionario con total_devices, avg_latency, critical_count,
        avg_bandwidth_mbps y avg_packet_loss_pct.
    """
    if df.empty:
        return {
            "total_devices": 0,
            "avg_latency": 0,
            "critical_count": 0,
            "avg_bandwidth_mbps": 0,
            "avg_packet_loss_pct": 0,
        }

    total_devices = int(df["device_id"].nunique())
    avg_latency = float(df["latency_ms"].mean())
    critical_count = int((df["status"] == "CRITICAL").sum())
    avg_bandwidth_mbps = float(df["bandwidth_mbps"].mean())
    avg_packet_loss_pct = float(df["packet_loss_pct"].mean())

    return {
        "total_devices": total_devices,
        "avg_latency": avg_latency,
        "critical_count": critical_count,
        "avg_bandwidth_mbps": avg_bandwidth_mbps,
        "avg_packet_loss_pct": avg_packet_loss_pct,
    }


def get_device_status(df: pd.DataFrame, window_minutes: int = 60) -> pd.DataFrame:
    """Retorna el último estado de cada dispositivo dentro de una ventana de tiempo.

    Args:
        df: DataFrame de métricas de red.
        window_minutes: Ventana de tiempo en minutos hacia atrás desde el
            timestamp máximo.

    Returns:
        DataFrame con el último registro por dispositivo dentro de la ventana.
    """
    if df.empty:
        return pd.DataFrame()

    df = df.copy()
    max_ts = df["timestamp"].max()
    cutoff = max_ts - pd.Timedelta(minutes=window_minutes)
    window_df = df[df["timestamp"] >= cutoff].copy()

    if window_df.empty:
        return pd.DataFrame()

    window_df = window_df.sort_values("timestamp")
    return window_df.drop_duplicates("device_id", keep="last").reset_index(drop=True)


def get_metrics_by_region(df: pd.DataFrame) -> pd.DataFrame:
    """Agrupa promedios de métricas numéricas por región.

    Args:
        df: DataFrame de métricas de red.

    Returns:
        DataFrame con promedios por región.
    """
    if df.empty:
        return pd.DataFrame()

    numeric_cols = [
        "latency_ms",
        "bandwidth_mbps",
        "packet_loss_pct",
        "cpu_usage_pct",
        "memory_usage_pct",
    ]

    return (
        df.groupby("region", as_index=False)[numeric_cols]
        .mean()
        .round(2)
        .sort_values("region")
    )

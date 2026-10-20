"""Lógica de evaluación de umbrales y generación de alertas."""

from __future__ import annotations

from typing import Final

import math
import pandas as pd

THRESHOLDS: Final[dict[str, dict[str, float]]] = {
    "latency_ms": {"warn": 20.0, "crit": 25.0},
    "cpu_usage_pct": {"warn": 80.0, "crit": 90.0},
    "packet_loss_pct": {"warn": 0.1, "crit": 0.2},
}

_SEVERITY_LABELS: Final[dict[str, str]] = {
    "crit": "CRÍTICO",
    "warn": "WARNING",
}


def check_thresholds(row: pd.Series) -> list[str]:
    """Evalúa los umbrales de una fila y retorna las alertas activas.

    Args:
        row: Fila (pd.Series) con las métricas de un dispositivo.

    Returns:
        Lista de strings con las alertas detectadas (vacía si todo está bien).
    """
    alerts: list[str] = []

    for column, limits in THRESHOLDS.items():
        if column not in row.index:
            continue

        value = row[column]

        if isinstance(value, float) and math.isnan(value):
            alerts.append(f"DATO FALTANTE: {column}")
            continue

        if value >= limits["crit"]:
            alerts.append(
                f"{_SEVERITY_LABELS['crit']}: {column} = {value} "
                f"(>= {limits['crit']})"
            )
        elif value >= limits["warn"]:
            alerts.append(
                f"{_SEVERITY_LABELS['warn']}: {column} = {value} "
                f"(>= {limits['warn']})"
            )

    return alerts


def get_active_alerts(df: pd.DataFrame) -> pd.DataFrame:
    """Filtra el último estado de cada dispositivo y aplica check_thresholds.

    Args:
        df: DataFrame de métricas de red.

    Returns:
        DataFrame con los dispositivos que tienen alertas activas, incluyendo
        una columna 'alertas' con la lista de alertas.
    """
    from utils.metrics import get_device_status

    status_df = get_device_status(df)

    if status_df.empty:
        return pd.DataFrame()

    records = []
    for _, row in status_df.iterrows():
        alerts = check_thresholds(row)
        if alerts:
            record = row.to_dict()
            record["alertas"] = alerts
            records.append(record)

    if not records:
        return pd.DataFrame()

    return pd.DataFrame(records).reset_index(drop=True)

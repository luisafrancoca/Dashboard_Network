import pandas as pd
import math
from utils.alerts import check_thresholds, get_active_alerts

def test_check_thresholds_ok():
    """Verifica que no lance alertas si los valores están en rango."""
    row = pd.Series({"latency_ms": 10, "cpu_usage_pct": 50})
    assert check_thresholds(row) == []

def test_check_thresholds_critical():
    """Verifica que detecte valores críticos."""
    row = pd.Series({"latency_ms": 35, "cpu_usage_pct": 90})
    alerts = check_thresholds(row)
    assert any("CRÍTICO" in a for a in alerts)

def test_check_thresholds_nan():
    """Verifica que detecte valores NaN (dato faltante)."""
    row = pd.Series({"latency_ms": math.nan, "cpu_usage_pct": 50})
    alerts = check_thresholds(row)
    assert any("DATO FALTANTE" in a for a in alerts)

def test_get_active_alerts():
    """Verifica que filtre dispositivos con alertas activas."""
    df = pd.DataFrame({
        "timestamp": pd.to_datetime(["2024-01-01 12:00:00", "2024-01-01 12:00:00"]),
        "device_id": ["RTR-001", "SW-001"],
        "device_name": ["Router 1", "Switch 1"],
        "region": ["North", "Center"],
        "latency_ms": [35.0, 10.0],
        "bandwidth_mbps": [100.0, 200.0],
        "packet_loss_pct": [0.01, 0.02],
        "cpu_usage_pct": [95.0, 50.0],
        "memory_usage_pct": [40.0, 45.0],
        "status": ["CRITICAL", "OK"],
    })
    result = get_active_alerts(df)
    assert len(result) == 1
    assert "CRÍTICO" in result["alertas"].iloc[0][0]

def test_get_active_alerts_none():
    """Verifica que retorne DataFrame vacío si no hay alertas activas."""
    df = pd.DataFrame({
        "timestamp": pd.to_datetime(["2024-01-01 12:00:00", "2024-01-01 12:00:00"]),
        "device_id": ["RTR-001", "SW-001"],
        "device_name": ["Router 1", "Switch 1"],
        "region": ["North", "Center"],
        "latency_ms": [10.0, 15.0],
        "bandwidth_mbps": [100.0, 200.0],
        "packet_loss_pct": [0.01, 0.02],
        "cpu_usage_pct": [50.0, 60.0],
        "memory_usage_pct": [40.0, 45.0],
        "status": ["OK", "OK"],
    })
    result = get_active_alerts(df)
    assert result.empty


def test_get_active_alerts_empty_df():
    """Verifica que retorne DataFrame vacío si el df de entrada está vacío."""
    result = get_active_alerts(pd.DataFrame())
    assert result.empty


def test_check_thresholds_warn():
    """Verifica que detecte valores en rango de advertencia (WARNING)."""
    row = pd.Series({"latency_ms": 22, "cpu_usage_pct": 50})
    alerts = check_thresholds(row)
    assert any("WARNING" in a for a in alerts)
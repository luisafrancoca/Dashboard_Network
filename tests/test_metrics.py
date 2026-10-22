import os
import tempfile
import pytest
import pandas as pd
from utils.metrics import load_data, get_summary_metrics, get_device_status, get_metrics_by_region

def test_load_data_file_not_found():
    """Verifica que lance FileNotFoundError si el CSV no existe."""
    with pytest.raises(FileNotFoundError):
        load_data("ruta/inexistente.csv")

def test_get_summary_metrics_empty_df():
    """Verifica que retorne ceros si el DataFrame está vacío."""
    df_empty = pd.DataFrame()
    result = get_summary_metrics(df_empty)
    
    assert result["total_devices"] == 0
    assert result["avg_latency"] == 0
    assert result["critical_count"] == 0

def test_get_device_status_last_timestamp():
    """Verifica que retorne solo el último registro por dispositivo dentro de la ventana."""
    df = pd.DataFrame({
        "timestamp": pd.to_datetime(["2024-01-01 10:00:00", "2024-01-01 11:00:00", "2024-01-01 12:00:00"]),
        "device_id": ["RTR-001", "RTR-001", "SW-001"],
        "device_name": ["Router 1", "Router 1", "Switch 1"],
        "region": ["North", "North", "Center"],
        "latency_ms": [10.0, 20.0, 15.0],
        "bandwidth_mbps": [100.0, 200.0, 150.0],
        "packet_loss_pct": [0.01, 0.02, 0.01],
        "cpu_usage_pct": [50.0, 60.0, 55.0],
        "memory_usage_pct": [40.0, 45.0, 42.0],
        "status": ["OK", "WARN", "OK"],
    })
    result = get_device_status(df, window_minutes=120)
    assert len(result) == 2
    rtr = result[result["device_id"] == "RTR-001"].iloc[0]
    assert rtr["latency_ms"] == 20.0

def test_get_device_status_empty_window():
    """Verifica que retorne DataFrame vacío si la ventana es negativa (no hay datos válidos)."""
    df = pd.DataFrame({
        "timestamp": pd.to_datetime(["2024-01-01 10:00:00"]),
        "device_id": ["RTR-001"],
        "device_name": ["Router 1"],
        "region": ["North"],
        "latency_ms": [10.0],
        "bandwidth_mbps": [100.0],
        "packet_loss_pct": [0.01],
        "cpu_usage_pct": [50.0],
        "memory_usage_pct": [40.0],
        "status": ["OK"],
    })
    result = get_device_status(df, window_minutes=-1)
    assert result.empty

def test_get_metrics_by_region():
    """Verifica que agrupe promedios por región correctamente."""
    df = pd.DataFrame({
        "timestamp": pd.to_datetime(["2024-01-01 10:00:00", "2024-01-01 11:00:00"]),
        "device_id": ["RTR-001", "SW-001"],
        "device_name": ["Router 1", "Switch 1"],
        "region": ["North", "Center"],
        "latency_ms": [10.0, 20.0],
        "bandwidth_mbps": [100.0, 200.0],
        "packet_loss_pct": [0.01, 0.02],
        "cpu_usage_pct": [50.0, 60.0],
        "memory_usage_pct": [40.0, 45.0],
        "status": ["OK", "OK"],
    })
    result = get_metrics_by_region(df)
    assert len(result) == 2
    assert "region" in result.columns
    assert "latency_ms" in result.columns

def test_get_metrics_by_region_empty_df():
    """Verifica que retorne DataFrame vacío si el df está vacío."""
    df_empty = pd.DataFrame()
    result = get_metrics_by_region(df_empty)
    assert result.empty


def test_load_data_success():
    """Verifica la ruta feliz de load_data con un CSV válido."""
    csv_content = """timestamp,device_id,device_name,region,latency_ms,bandwidth_mbps,packet_loss_pct,cpu_usage_pct,memory_usage_pct,status
2024-01-01 10:00:00,RTR-001,Router 1,North,10.0,100.0,0.01,50.0,40.0,OK
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(csv_content)
        tmp_path = f.name
    try:
        result = load_data(tmp_path)
        assert len(result) == 1
        assert result.iloc[0]["device_id"] == "RTR-001"
        assert pd.api.types.is_datetime64_any_dtype(result["timestamp"])
    finally:
        os.unlink(tmp_path)


def test_get_summary_metrics_non_empty():
    """Verifica que calcule los 5 KPIs con un df no vacío."""
    df = pd.DataFrame({
        "device_id": ["RTR-001", "RTR-002"],
        "latency_ms": [10.0, 20.0],
        "status": ["OK", "CRITICAL"],
        "bandwidth_mbps": [100.0, 200.0],
        "packet_loss_pct": [0.01, 0.02],
    })
    result = get_summary_metrics(df)
    assert result["total_devices"] == 2
    assert result["avg_latency"] == 15.0
    assert result["critical_count"] == 1


def test_get_device_status_empty_df():
    """Verifica que retorne DataFrame vacío si el df de entrada está vacío."""
    result = get_device_status(pd.DataFrame())
    assert result.empty
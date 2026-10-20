import pandas as pd
import math
from utils.alerts import check_thresholds

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
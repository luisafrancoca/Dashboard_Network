import pytest
import pandas as pd
from utils.metrics import load_data, get_summary_metrics

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
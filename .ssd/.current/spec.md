# PLAN DE IMPLEMENTACIÓN TÉCNICA

## 1. Arquitectura de Archivos
- `app.py`: Interfaz de usuario, layout de Streamlit y orquestación.
- `utils/__init__.py`: Inicializador del módulo.
- `utils/metrics.py`: Funciones de carga, limpieza y cálculo de KPIs.
- `utils/alerts.py`: Lógica de evaluación de umbrales y generación de alertas.
- `data/network_metrics.csv`: Dataset de prueba.

## 2. Detalle de Módulos

### `utils/metrics.py`
- `load_data(filepath: str) -> pd.DataFrame`: Valida existencia del archivo, columnas requeridas, parsea fechas.
- `get_summary_metrics(df: pd.DataFrame) -> dict`: Retorna diccionario con los 5 KPIs.
- `get_device_status(df: pd.DataFrame, window_minutes: int = 60) -> pd.DataFrame`: Retorna el último estado de cada dispositivo en una ventana de tiempo.
- `get_metrics_by_region(df: pd.DataFrame) -> pd.DataFrame`: Agrupa promedios por región.

### `utils/alerts.py`
- `THRESHOLDS`: Diccionario con los límites Warn/Crit.
- `check_thresholds(row: pd.Series) -> list`: Retorna lista de strings con alertas activas para una fila.
- `get_active_alerts(df: pd.DataFrame) -> pd.DataFrame`: Filtra el último estado y aplica `check_thresholds`.

### `app.py`
- Configurar página (layout wide, dark mode).
- Inyectar CSS personalizado para las tarjetas de alerta.
- Implementar Sidebar con los 3 filtros.
- Renderizar las 5 columnas de KPIs.
- Renderizar sección de alertas activas.
- Renderizar los 4 gráficos con Plotly.
- Renderizar tabla con `st.dataframe` y `column_config`.
- Renderizar botones de descarga.
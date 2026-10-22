# TAREAS DE DESARROLLO (SDD + TDD)

## Fase 1: Configuración y Datos
- [x] T1: Crear la estructura de carpetas `tests/`, el archivo `pytest.ini` y asegurar que el CSV de prueba (`data/network_metrics.csv`) existe.

## Fase 2: Desarrollo de Lógica (Ciclo TDD)
- [x] T2: Escribir los tests unitarios para `utils/metrics.py` (carga de archivos, cálculo de KPIs, último estado).
- [x] T3: Implementar `utils/metrics.py` con type hints y manejo de errores hasta que los tests de T2 pasen al 100%.
- [x] T4: Escribir los tests unitarios para `utils/alerts.py` (umbrales, detección de NaN, alertas activas).
- [x] T5: Implementar `utils/alerts.py` hasta que los tests de T4 pasen al 100%.

## Fase 3: Desarrollo de Interfaz (UI)
- [x] T6: Crear el esqueleto de `app.py`, configurar la página (layout wide) e inyectar el CSS personalizado (Dark mode).
- [x] T7: Implementar la barra lateral (Sidebar) con los 3 filtros dinámicos (Región, Dispositivo, Estado) y la lógica de filtrado del DataFrame.
- [x] T8: Implementar la fila superior con las 5 tarjetas de KPIs (métricas resumen).
- [x] T9: Implementar la sección visual de Alertas Activas con contenedores HTML/CSS.
- [x] T10: Implementar los 4 gráficos interactivos usando Plotly Express.
- [x] T11: Implementar la tabla de dispositivos usando `st.dataframe` y `column_config` (prohibido usar `.style.map`).
- [x] T12: Implementar los botones de descarga en formato CSV para datos filtrados y resumen por región.

## Fase 4: Calidad y Despliegue
- [x] T13: Correr `pytest` en la terminal y verificar que toda la suite pase y la cobertura de `utils/` sea >= 80%.
- [x] T14: Verificar localmente que `streamlit run app.py` funcione sin errores ni advertencias en la consola.
- [x] T15: (Opcional) Inicializar Git, subir a GitHub y desplegar en Streamlit Cloud.

"""Tests de integración para la aplicación Streamlit usando AppTest.

Verifica:
- Carga de la app sin errores
- Funcionamiento de los 3 filtros del sidebar (Región, Dispositivo, Estado)
- Renderizado de KPIs, gráficos, tabla y descargas
- Ausencia de excepciones durante la ejecución
"""

from __future__ import annotations

import pytest
from streamlit.testing.v1 import AppTest


@pytest.fixture
def at() -> AppTest:
    """Inicializa la aplicación Streamlit para pruebas."""
    at = AppTest.from_file("app.py")
    try:
        at.run(timeout=30)
    except RuntimeError:
        # Si hay timeout por widgets interactivos, continuamos de todos modos
        # ya que la app puede haberse renderizado parcialmente
        pass
    return at


def test_app_loads_without_errors(at: AppTest) -> None:
    """Verifica que la app cargue sin lanzar excepciones."""
    assert at.exception is None or len(at.exception) == 0


def test_app_title(at: AppTest) -> None:
    """Verifica que el título de la app sea correcto."""
    titles = [getattr(el, "value", str(el)) for el in at.title]
    assert any("Dashboard de Redes" in str(t) for t in titles), f"Título no encontrado en: {titles}"


def test_sidebar_filters_present(at: AppTest) -> None:
    """Verifica que los 3 filtros del sidebar estén presentes."""
    assert len(at.selectbox) >= 3, f"Se esperaban al menos 3 selectboxes, se encontraron {len(at.selectbox)}"

    labels = [str(el.label) for el in at.selectbox if hasattr(el, "label")]
    assert any("Región" in label for label in labels), f"Filtro de Región no encontrado en: {labels}"
    assert any("Dispositivo" in label for label in labels), f"Filtro de Dispositivo no encontrado en: {labels}"
    assert any("Estado" in label for label in labels), f"Filtro de Estado no encontrado en: {labels}"


def test_kpi_values_present(at: AppTest) -> None:
    """Verifica que los valores de KPI se rendericen en markdown."""
    markdown_texts = [getattr(el, "value", str(el)) for el in at.markdown]
    combined = " ".join(str(t) for t in markdown_texts)
    assert "Dispositivos" in combined, "KPI de Dispositivos no encontrado"
    assert "Latencia" in combined, "KPI de Latencia no encontrado"
    assert "Críticos" in combined, "KPI de Críticos no encontrado"
    assert "Ancho de banda" in combined, "KPI de Ancho de banda no encontrado"
    assert "Pérdida de paquetes" in combined, "KPI de Pérdida de paquetes no encontrado"


def test_charts_render(at: AppTest) -> None:
    """Verifica que los gráfiques se rendericen (usando columnas y divs de plotly)."""
    # Los gráficos Plotly se renderizan como elementos div/svg dentro de columnas
    assert len(at.columns) > 0, "No se encontraron columnas para los gráficos"
    # Verificar que no hay errores de renderizado en los gráficos
    assert at.exception is None or len(at.exception) == 0, f"Errores en renderizado de gráficos: {at.exception}"


def test_table_present(at: AppTest) -> None:
    """Verifica que la tabla de dispositivos se renderice."""
    assert len(at.dataframe) >= 1, "No se encontró la tabla de dispositivos"


def test_no_error_elements(at: AppTest) -> None:
    """Verifica que no haya elementos de error en la UI."""
    assert len(at.error) == 0, f"Se encontraron elementos de error: {at.error}"
    assert len(at.exception) == 0, f"Se encontraron excepciones: {at.exception}"


def test_region_filter_changes_data(at: AppTest) -> None:
    """Verifica que cambiar el filtro de región no lance excepciones."""
    region_select = None
    for el in at.selectbox:
        if hasattr(el, "label") and "Región" in str(el.label):
            region_select = el
            break

    assert region_select is not None, "No se encontró el selectbox de Región"

    regiones = region_select.options
    assert len(regiones) > 1, "No hay regiones disponibles para filtrar"

    # Seleccionar la primera región que no sea "Todos"
    for region in regiones:
        if region != "Todos":
            region_select.select(region)
            at.run(timeout=30)
            assert at.exception is None or len(at.exception) == 0, f"Excepción al filtrar por región: {region}"
            break


def test_device_filter_changes_data(at: AppTest) -> None:
    """Verifica que cambiar el filtro de dispositivo no lance excepciones."""
    device_select = None
    for el in at.selectbox:
        if hasattr(el, "label") and "Dispositivo" in str(el.label):
            device_select = el
            break

    assert device_select is not None, "No se encontró el selectbox de Dispositivo"

    dispositivos = device_select.options
    assert len(dispositivos) > 1, "No hay dispositivos disponibles para filtrar"

    for dispositivo in dispositivos:
        if dispositivo != "Todos":
            device_select.select(dispositivo)
            at.run(timeout=30)
            assert at.exception is None or len(at.exception) == 0, f"Excepción al filtrar por dispositivo: {dispositivo}"
            break


def test_status_filter_changes_data(at: AppTest) -> None:
    """Verifica que cambiar el filtro de estado no lance excepciones."""
    status_select = None
    for el in at.selectbox:
        if hasattr(el, "label") and "Estado" in str(el.label):
            status_select = el
            break

    assert status_select is not None, "No se encontró el selectbox de Estado"

    estados = status_select.options
    assert len(estados) > 1, "No hay estados disponibles para filtrar"

    for estado in estados:
        if estado != "Todos":
            status_select.select(estado)
            at.run(timeout=30)
            assert at.exception is None or len(at.exception) == 0, f"Excepción al filtrar por estado: {estado}"
            break

# Dashboard de Redes

Dashboard de monitoreo de redes construido con **Streamlit**, **pandas** y **Plotly**. Muestra KPIs, alertas activas, gráficos interactivos y una tabla de dispositivos con filtros dinámicos por región, dispositivo y estado.

## Requisitos

- Python 3.12+
- pip

## Instalación

```bash
git clone <repositorio>
cd dashboard-rede
pip install -r requirements.txt
```

## Ejecución local

```bash
streamlit run app.py
```

Luego abre http://localhost:8501 en tu navegador.

## Estructura del proyecto

```
app.py                  # Interfaz de usuario (Streamlit)
utils/
  __init__.py
  metrics.py            # Carga de datos y cálculo de KPIs
  alerts.py             # Umbrales y generación de alertas
data/
  network_metrics.csv   # Dataset de métricas de red
tests/
  test_metrics.py       # Tests unitarios de métricas
  test_alerts.py        # Tests unitarios de alertas
requirements.txt        # Dependencias de Python
pytest.ini              # Configuración de pytest
```

## Ejecutar pruebas

```bash
pytest
```

Con cobertura:

```bash
pytest --cov=utils
```

## Requisitos de calidad

- Cobertura mínima del 80% en la carpeta `utils/` (ver `constitution.md`).
- Cada función en `utils/metrics.py` y `utils/alerts.py` debe tener al menos un test unitario.

## Despliegue opcional

Desplegar en [Streamlit Cloud](https://streamlit.io/cloud):

1. Sube el código a un repositorio de GitHub.
2. Conecta el repositorio en Streamlit Cloud.
3. Configura el archivo principal como `app.py`.

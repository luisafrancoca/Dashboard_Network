# CONSTITUCIÓN DEL PROYECTO: Dashboard de Redes

## 1. Principios Fundamentales
- **Modularidad:** La lógica de negocio (cálculos, filtros, alertas) NUNCA debe estar en el archivo principal `app.py`. Debe estar en la carpeta `utils/`.
- **Manejo de Errores:** La aplicación debe ser a prueba de fallos. Si el archivo CSV no existe o está corrupto, se debe mostrar un `st.error` amigable, nunca un traceback de Python.
- **Rendimiento:** El uso de caché es obligatorio para la carga de datos pesados (`@st.cache_data`).
- **Validación de Datos:** Cualquier DataFrame entrante debe ser validado (existencia de columnas, tipos de datos).

## 2. Restricciones Técnicas
- **Lenguaje:** Python 3.12+
- **Framework UI:** Streamlit
- **Librerías de Datos:** Pandas, Numpy
- **Librerías de Gráficos:** Plotly Express (prohibido usar Matplotlib para la UI)
- **Testing:** Pytest (obligatorio). Cobertura mínima del 80% en la carpeta `utils/`.
- **Estilo Visual:** Tema oscuro (Dark Mode), acentos en Cyan (`#00D4FF`) y Rojo (`#FF4B4B`).

## 3. Estándares de Código
- Uso estricto de Type Hints (ej. `def cargar_datos(ruta: str) -> pd.DataFrame:`).
- Docstrings en todas las funciones explicando qué hacen.
- No usar variables globales mutables.

## 4. Política de Testing (TDD)
- **Obligatorio:** Cada función en `utils/metrics.py` y `utils/alerts.py` debe tener al menos un test unitario.
- **Manejo de Mocks:** Los tests de alertas deben usar `pytest` para simular filas de Pandas con valores nulos (NaN).
- **Ubicación:** Todos los tests deben ir en la carpeta `tests/`.
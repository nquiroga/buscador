# 📚 Búsqueda Académica Avanzada - OpenAlex

**Seminario de tesis - Etapa Avanzada. 2025**

Aplicación web interactiva para realizar búsquedas académicas avanzadas usando la API gratuita de OpenAlex, con soporte para operadores booleanos y exportación optimizada para NotebookLM.

## 🚀 Características

- ✅ **Búsquedas Booleanas Avanzadas**: Soporte completo para operadores AND, OR, NOT
- ✅ **Hasta 500 resultados por búsqueda**: Límite configurable
- ✅ **Exportación a Markdown**: Formato optimizado para NotebookLM
- ✅ **Exportación a CSV**: Para análisis en Excel/Python
- ✅ **Interfaz intuitiva**: Con guía de uso integrada
- ✅ **Tres modos de búsqueda**: Título y Abstract, General, Solo Título
- ✅ **Visualización detallada**: Vista de tabla + detalle individual
- ✅ **100% Gratuito**: Sin necesidad de API keys o suscripciones

## 📋 Requisitos

- Python 3.8 o superior
- Conexión a internet

## 🔧 Instalación Local

1. Clone el repositorio o descargue los archivos:
```bash
git clone [tu-repositorio]
cd red_peronismo
```

2. Instale las dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecute la aplicación:
```bash
streamlit run app_streamlit.py
```

4. Abra su navegador en `http://localhost:8501`

## ☁️ Deployment en Streamlit Cloud

### Paso 1: Preparar el repositorio en GitHub

1. Suba estos archivos a su repositorio de GitHub:
   - `app_streamlit.py`
   - `openalex_search.py`
   - `requirements.txt`
   - `.streamlit/config.toml` (opcional)
   - `README_STREAMLIT.md`

### Paso 2: Conectar con Streamlit Cloud

1. Vaya a [share.streamlit.io](https://share.streamlit.io)
2. Inicie sesión con su cuenta de GitHub
3. Click en "New app"
4. Configure:
   - **Repository**: Seleccione su repositorio
   - **Branch**: `main` (o su rama principal)
   - **Main file path**: `app_streamlit.py`
5. Click en "Deploy"

### Paso 3: Configuración Avanzada (Opcional)

Si necesita configuración adicional, cree un archivo `.streamlit/secrets.toml`:

```toml
# Agregar si necesita configuraciones secretas en el futuro
# Por ahora no es necesario
```

## 📖 Guía de Uso

### Operadores Booleanos

La aplicación soporta los siguientes operadores (deben estar en MAYÚSCULAS):

- **AND**: Ambos términos deben aparecer
  ```
  peronismo AND argentina
  ```

- **OR**: Al menos uno debe aparecer
  ```
  "Juan Perón" OR "Eva Perón"
  ```

- **NOT**: Excluye resultados
  ```
  peronismo NOT militar
  ```

- **Paréntesis**: Controla el orden de operaciones
  ```
  (peronismo OR justicialismo) AND argentina
  ```

### Tipos de Búsqueda

1. **Título y Abstract**: Busca en el título y resumen del artículo (recomendado)
2. **General**: Busca en todo el documento disponible
3. **Solo Título**: Búsqueda únicamente en títulos

### Frases Exactas

Use comillas dobles para buscar frases exactas:
```
"historia argentina contemporánea"
```

### Búsqueda Multilingüe

Separe términos con comas para búsqueda OR automática:
```
peronismo, peronism, justicialismo
```
Se convierte automáticamente a: `peronismo OR peronism OR justicialismo`

## 📊 Exportación de Resultados

### Formato CSV
- Ideal para análisis en Excel, Python, R
- Incluye todas las columnas: título, autores, publicación, año, DOI, abstract, citaciones, etc.

### Formato Markdown (para NotebookLM)
- Formato optimizado para cargar en Google NotebookLM
- Estructura clara con título, autores, abstract y metadata
- Un documento completo listo para análisis de IA

## 🎯 Ejemplos de Consultas

### Ejemplo 1: Búsqueda Simple
```
peronismo
```

### Ejemplo 2: Búsqueda Multilingüe
```
peronismo, peronism
```

### Ejemplo 3: Búsqueda Booleana
```
(peronismo OR justicialismo) AND argentina
```

### Ejemplo 4: Excluir Términos
```
peronismo NOT militar
```

### Ejemplo 5: Frase Exacta + Booleano
```
"Juan Perón" AND (política OR economía)
```

## 📈 Capacidades y Límites

### ✅ Capacidades
- Búsqueda en 240+ millones de trabajos académicos
- 100,000 requests/día (gratuitos)
- Sin necesidad de API key
- Soporte multilingüe
- Deduplicación automática
- Búsqueda completa en abstracts

### ⚠️ Límites
- Máximo 500 resultados por búsqueda (límite de la app)
- Aproximadamente 50% de trabajos tienen abstract completo
- No incluye texto completo de artículos (solo metadata)

## 🛠️ Estructura del Proyecto

```
red_peronismo/
├── app_streamlit.py          # Aplicación principal Streamlit
├── openalex_search.py         # Módulo de búsqueda OpenAlex
├── requirements.txt           # Dependencias Python
├── .streamlit/
│   └── config.toml           # Configuración de Streamlit
├── README_STREAMLIT.md       # Esta documentación
└── README_OpenAlex.md        # Documentación de la API
```

## 🔍 Solución de Problemas

### Error: "Module not found"
```bash
pip install -r requirements.txt
```

### La aplicación no inicia
Verifique que está usando Python 3.8+:
```bash
python --version
```

### No se encuentran resultados
- Verifique que los operadores booleanos estén en MAYÚSCULAS (AND, OR, NOT)
- Pruebe con términos más generales
- Revise la sintaxis de su consulta

### Error de conexión
- Verifique su conexión a internet
- OpenAlex API puede estar temporalmente no disponible

## 📚 Recursos Adicionales

- [Documentación de OpenAlex API](https://docs.openalex.org/)
- [Documentación de Streamlit](https://docs.streamlit.io/)
- [OpenAlex API Tutorials](https://github.com/ourresearch/openalex-api-tutorials)
- [NotebookLM de Google](https://notebooklm.google/)

## 🤝 Contribuciones

Este proyecto fue desarrollado para el Seminario de tesis - Etapa Avanzada. 2025.

## 📄 Licencia

Este proyecto utiliza:
- **OpenAlex API**: Datos bajo licencia CC0 (dominio público)
- **Código**: Disponible para uso académico

## 📧 Soporte

Para reportar problemas o sugerencias, consulte la documentación de OpenAlex o Streamlit.

---

**Desarrollado con ❤️ para investigadores académicos**

*Powered by OpenAlex API - Una alternativa gratuita y abierta para la investigación académica*

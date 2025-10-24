"""
Seminario de tesis - Etapa Avanzada. 2025
Herramienta de Búsqueda Académica con OpenAlex API
Permite búsquedas avanzadas con operadores booleanos y exportación a Markdown
"""

import streamlit as st
import pandas as pd
from openalex_search import OpenAlexSearcher
from datetime import datetime
import io

# Configuración de la página
st.set_page_config(
    page_title="Búsqueda Académica - OpenAlex",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("📚 Búsqueda Académica Avanzada")
st.caption("Seminario de tesis - Etapa Avanzada. 2025")

# Sidebar con ayuda
with st.sidebar:
    st.header("📖 Guía de Uso")

    st.subheader("Operadores Booleanos")
    st.markdown("""
    **Operadores disponibles (MAYÚSCULAS):**
    - `AND` - Ambos términos deben aparecer
    - `OR` - Al menos uno debe aparecer
    - `NOT` - Excluye resultados

    **Ejemplos:**
    - `peronismo AND argentina`
    - `"Juan Perón" OR "Eva Perón"`
    - `peronismo NOT militar`
    - `(peronismo OR justicialismo) AND argentina`
    """)

    st.subheader("Búsqueda Avanzada")
    st.markdown("""
    **Frases exactas:**
    - Use comillas: `"historia argentina"`

    **Múltiples términos (OR automático):**
    - Separe con comas: `peronismo, justicialismo`
    - Se convierte a: `peronismo OR justicialismo`

    **Paréntesis:**
    - Controla el orden: `(A OR B) AND C`
    """)

    st.subheader("Tipos de Búsqueda")
    st.markdown("""
    - **Título y Abstract**: Busca en título y resumen
    - **General**: Busca en todo el documento
    - **Solo Título**: Busca únicamente en títulos
    """)

    st.subheader("Limitaciones")
    st.info("⚠️ Máximo: 500 resultados por búsqueda")

# Formulario de búsqueda
st.header("🔍 Nueva Búsqueda")

col1, col2 = st.columns([3, 1])

with col1:
    query = st.text_input(
        "Ingrese su consulta de búsqueda",
        placeholder='Ej: (peronismo OR justicialismo) AND argentina',
        help="Use operadores booleanos (AND, OR, NOT) y comillas para frases exactas"
    )

with col2:
    search_type = st.selectbox(
        "Tipo de búsqueda",
        ["title_abstract", "general", "title_only"],
        format_func=lambda x: {
            "title_abstract": "Título y Abstract",
            "general": "General",
            "title_only": "Solo Título"
        }[x]
    )

col3, col4 = st.columns([1, 1])

with col3:
    max_results = st.number_input(
        "Cantidad de resultados",
        min_value=10,
        max_value=500,
        value=100,
        step=10,
        help="Máximo 500 resultados"
    )

with col4:
    sort_by = st.selectbox(
        "Ordenar por",
        ["relevance_score:desc", "cited_by_count:desc", "publication_year:desc"],
        format_func=lambda x: {
            "relevance_score:desc": "Relevancia",
            "cited_by_count:desc": "Más citados",
            "publication_year:desc": "Más recientes"
        }[x]
    )

# Botón de búsqueda
search_button = st.button("🔍 Buscar", type="primary", use_container_width=True)

# Función para convertir resultados a Markdown
def convert_to_markdown(results_df):
    """Convierte los resultados a formato Markdown optimizado para NotebookLM"""

    md_content = f"""# Resultados de Búsqueda Académica

**Consulta:** {results_df['search_query'].iloc[0] if len(results_df) > 0 else 'N/A'}
**Fecha de búsqueda:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total de resultados:** {len(results_df)}
**Fuente:** OpenAlex API

---

"""

    for idx, row in results_df.iterrows():
        md_content += f"""## {idx + 1}. {row['title']}

**Autores:** {row['author'] if row['author'] else 'N/A'}
**Publicación:** {row['publication'] if row['publication'] else 'N/A'}
**Año:** {row['year']}
**Citaciones:** {row['citations']}
**DOI:** {row['doi'] if row['doi'] else 'N/A'}
**OpenAlex ID:** {row['openalex_id']}
**Acceso Abierto:** {'Sí' if row['open_access'] else 'No'}

### Abstract

{row['abstract'] if row['abstract'] else 'No disponible'}

---

"""

    return md_content

# Realizar búsqueda
if search_button:
    if not query:
        st.error("⚠️ Por favor ingrese una consulta de búsqueda")
    else:
        with st.spinner("🔄 Buscando en OpenAlex..."):
            try:
                # Inicializar el buscador
                searcher = OpenAlexSearcher()

                # Realizar búsqueda
                results = searcher.get_all_results(
                    query=query,
                    max_results=max_results,
                    search_type=search_type
                )

                if not results:
                    st.warning("No se encontraron resultados para esta búsqueda")
                else:
                    # Convertir a DataFrame
                    df = pd.DataFrame(results)

                    # Guardar en session state
                    st.session_state['results'] = df
                    st.session_state['query'] = query

                    st.success(f"✅ Se encontraron {len(df)} resultados")

            except Exception as e:
                st.error(f"❌ Error durante la búsqueda: {str(e)}")

# Mostrar resultados
if 'results' in st.session_state and st.session_state['results'] is not None:
    df = st.session_state['results']

    st.header("📊 Resultados")

    # Estadísticas
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de resultados", len(df))
    col2.metric("Con abstract", df['abstract'].notna().sum())
    col3.metric("Acceso abierto", df['open_access'].sum())
    col4.metric("Promedio de citas", int(df['citations'].astype(float).mean()))

    # Botones de descarga
    st.subheader("💾 Exportar Resultados")

    col1, col2 = st.columns(2)

    with col1:
        # Descargar CSV
        csv = df.to_csv(index=False, encoding='utf-8')
        st.download_button(
            label="📥 Descargar CSV",
            data=csv,
            file_name=f"resultados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col2:
        # Descargar Markdown
        markdown = convert_to_markdown(df)
        st.download_button(
            label="📥 Descargar Markdown (para NotebookLM)",
            data=markdown,
            file_name=f"resultados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
            use_container_width=True
        )

    # Tabla de resultados
    st.subheader("📋 Vista de Resultados")

    # Configurar columnas a mostrar
    display_columns = ['title', 'author', 'publication', 'year', 'citations', 'open_access']

    # Crear DataFrame para mostrar
    display_df = df[display_columns].copy()
    display_df['open_access'] = display_df['open_access'].map({True: '✅', False: '❌'})

    # Renombrar columnas
    display_df.columns = ['Título', 'Autores', 'Publicación', 'Año', 'Citas', 'Acceso Abierto']

    st.dataframe(
        display_df,
        use_container_width=True,
        height=400
    )

    # Detalle de resultados individuales
    st.subheader("🔍 Ver Detalle Individual")

    selected_index = st.selectbox(
        "Seleccione un resultado para ver el detalle completo",
        options=range(len(df)),
        format_func=lambda x: f"{x+1}. {df.iloc[x]['title'][:80]}..."
    )

    if selected_index is not None:
        selected = df.iloc[selected_index]

        with st.expander("📄 Detalle Completo", expanded=True):
            st.markdown(f"### {selected['title']}")
            st.markdown(f"**Autores:** {selected['author']}")
            st.markdown(f"**Publicación:** {selected['publication']}")
            st.markdown(f"**Año:** {selected['year']}")
            st.markdown(f"**Citaciones:** {selected['citations']}")
            st.markdown(f"**DOI:** {selected['doi'] if selected['doi'] else 'N/A'}")
            st.markdown(f"**OpenAlex ID:** {selected['openalex_id']}")
            st.markdown(f"**Acceso Abierto:** {'Sí' if selected['open_access'] else 'No'}")

            st.markdown("#### Abstract")
            st.write(selected['abstract'] if selected['abstract'] else "No disponible")

# Footer
st.divider()
st.caption("Seminario de tesis - Etapa Avanzada. 2025 | Datos de OpenAlex API")

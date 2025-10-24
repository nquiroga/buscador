"""
Búsqueda en OpenAlex - Alternativa gratuita a Scopus
No requiere API key, búsqueda completa en título y abstract
"""

import requests
import pandas as pd
import json
from datetime import datetime
from typing import List, Dict, Optional


class OpenAlexSearcher:
    """Cliente para realizar búsquedas en OpenAlex API"""
    
    def __init__(self, email: str = None):
        """
        Inicializa el cliente de búsqueda
        
        Args:
            email: Email opcional para mejores tiempos de respuesta
        """
        self.base_url = 'https://api.openalex.org/works'
        self.email = email
        self.session = requests.Session()
        
        # Configurar headers básicos
        self.session.headers.update({
            'User-Agent': 'OpenAlexSearcher/1.0'
        })
    
    def _format_query_for_openalex(self, query: str) -> str:
        """
        Formatea la consulta para OpenAlex API
        
        Args:
            query: Consulta del usuario
            
        Returns:
            Consulta formateada para OpenAlex
        """
        # Si contiene comas, convertir a OR
        if ',' in query and 'OR' not in query.upper() and 'AND' not in query.upper():
            terms = [term.strip() for term in query.split(',') if term.strip()]
            # Limpiar términos y agregar comillas si es necesario
            formatted_terms = []
            for term in terms:
                term = term.strip()
                if term and not (term.startswith('"') and term.endswith('"')):
                    if ' ' in term:
                        formatted_terms.append(f'"{term}"')
                    else:
                        formatted_terms.append(term)
                elif term:
                    formatted_terms.append(term)
            return ' OR '.join(formatted_terms)
        
        return query

    def search_title_abstract(
        self, 
        query: str, 
        per_page: int = 200,
        page: int = 1,
        sort: str = 'relevance_score:desc'
    ) -> Dict:
        """
        Busca en título y abstract usando OpenAlex
        
        Args:
            query: Término de búsqueda
            per_page: Resultados por página (máx 200)
            page: Número de página
            sort: Criterio de ordenamiento
            
        Returns:
            Diccionario con los resultados de la búsqueda
        """
        # Formatear consulta
        formatted_query = self._format_query_for_openalex(query)
        
        params = {
            'filter': f'title_and_abstract.search:{formatted_query}',
            'per-page': min(per_page, 200),
            'page': page,
            'sort': sort,
            'select': 'id,display_name,publication_year,primary_location,authorships,abstract_inverted_index,cited_by_count,doi,open_access'
        }
        
        # Remover mailto ya que causa error 400
        
        try:
            response = self.session.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return {'error': f'Error en la solicitud: {str(e)}'}
    
    def search_general(
        self, 
        query: str, 
        per_page: int = 200,
        page: int = 1
    ) -> Dict:
        """
        Búsqueda general en título, abstract y texto completo
        
        Args:
            query: Término de búsqueda
            per_page: Resultados por página
            page: Número de página
            
        Returns:
            Diccionario con los resultados
        """
        # Formatear consulta
        formatted_query = self._format_query_for_openalex(query)
        
        params = {
            'search': formatted_query,
            'per-page': min(per_page, 200),
            'page': page,
            'select': 'id,display_name,publication_year,primary_location,authorships,abstract_inverted_index,cited_by_count,doi,open_access'
        }
        
        # Remover mailto ya que causa error 400
        
        try:
            response = self.session.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return {'error': f'Error en la solicitud: {str(e)}'}
    
    def search_title_only(self, query: str, per_page: int = 200) -> Dict:
        """Busca solo en título"""
        # Formatear consulta
        formatted_query = self._format_query_for_openalex(query)
        
        params = {
            'filter': f'title.search:{formatted_query}',
            'per-page': min(per_page, 200),
            'select': 'id,display_name,publication_year,primary_location,authorships,abstract_inverted_index,cited_by_count,doi,open_access'
        }
        
        # Remover mailto ya que causa error 400
            
        try:
            response = self.session.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': f'Error en la solicitud: {str(e)}'}
    
    def parse_results(self, search_results: Dict, query: str = '') -> List[Dict]:
        """
        Extrae información relevante de los resultados
        
        Args:
            search_results: Resultados crudos de la API
            query: Término de búsqueda usado
            
        Returns:
            Lista de diccionarios con información simplificada
        """
        if 'error' in search_results:
            return []
        
        if 'results' not in search_results:
            return []
        
        parsed_results = []
        search_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        for work in search_results['results']:
            # Extraer información del autor principal
            authors = []
            if work.get('authorships'):
                for auth in work['authorships'][:3]:  # Primeros 3 autores
                    author_name = auth.get('author', {}).get('display_name', '')
                    if author_name:
                        authors.append(author_name)
            
            # Extraer información de la publicación
            primary_location = work.get('primary_location', {}) or {}
            source_info = primary_location.get('source', {}) or {}
            
            # Convertir abstract invertido a texto plano
            abstract_text = self._convert_inverted_abstract(
                work.get('abstract_inverted_index', {})
            )
            
            result = {
                'title': work.get('display_name', ''),
                'author': '; '.join(authors) if authors else '',
                'publication': source_info.get('display_name', ''),
                'year': str(work.get('publication_year', '')),
                'doi': work.get('doi', ''),
                'abstract': abstract_text,
                'citations': str(work.get('cited_by_count', 0)),
                'openalex_id': work.get('id', '').replace('https://openalex.org/', ''),
                'open_access': work.get('open_access', {}).get('is_oa', False),
                'search_query': query,
                'search_date': search_date,
                'source': 'OpenAlex'
            }
            parsed_results.append(result)
        
        return parsed_results
    
    def _convert_inverted_abstract(self, inverted_index: Dict) -> str:
        """
        Convierte el abstract invertido de OpenAlex a texto plano
        
        Args:
            inverted_index: Diccionario con palabras y posiciones
            
        Returns:
            Texto del abstract reconstruido
        """
        if not inverted_index:
            return ''
        
        # Crear lista de palabras ordenadas por posición
        word_positions = []
        for word, positions in inverted_index.items():
            for pos in positions:
                word_positions.append((pos, word))
        
        # Ordenar por posición y unir
        word_positions.sort(key=lambda x: x[0])
        abstract = ' '.join([word for _, word in word_positions])
        
        return abstract[:500] + '...' if len(abstract) > 500 else abstract
    
    def get_all_results(
        self, 
        query: str, 
        max_results: int = 2000,
        search_type: str = 'title_abstract'
    ) -> List[Dict]:
        """
        Obtiene todos los resultados disponibles (paginación automática)
        
        Args:
            query: Término de búsqueda
            max_results: Máximo número de resultados a obtener
            search_type: 'title_abstract', 'general', o 'title_only'
            
        Returns:
            Lista con todos los resultados encontrados
        """
        all_results = []
        page = 1
        per_page = 200
        
        print(f"Obteniendo resultados de OpenAlex para '{query}'...")
        
        while len(all_results) < max_results:
            # Seleccionar método de búsqueda
            if search_type == 'title_abstract':
                batch = self.search_title_abstract(query, per_page, page)
            elif search_type == 'general':
                batch = self.search_general(query, per_page, page)
            elif search_type == 'title_only':
                batch = self.search_title_only(query, per_page)
            else:
                raise ValueError("search_type debe ser 'title_abstract', 'general', o 'title_only'")
            
            if 'error' in batch:
                print(f"ERROR: {batch['error']}")
                break
            
            if not batch.get('results'):
                print("No hay mas resultados")
                break
            
            # Procesar resultados de esta página
            parsed_batch = self.parse_results(batch, query)
            all_results.extend(parsed_batch)
            
            # Mostrar progreso
            total_available = batch.get('meta', {}).get('count', 0)
            print(f"Descargados: {len(all_results)}/{min(max_results, total_available)}")
            
            # Verificar si hay más páginas
            if len(parsed_batch) < per_page:
                break
            
            page += 1
        
        print(f"Descarga completa: {len(all_results)} resultados")
        return all_results[:max_results]
    
    def save_to_csv(
        self, 
        query: str, 
        csv_filename: str = 'openalex_results.csv',
        max_results: int = 2000,
        search_type: str = 'title_abstract'
    ) -> Dict:
        """
        Busca y guarda resultados en CSV con deduplicación
        
        Args:
            query: Término de búsqueda
            csv_filename: Nombre del archivo CSV
            max_results: Máximo resultados a obtener
            search_type: Tipo de búsqueda
            
        Returns:
            Diccionario con estadísticas
        """
        # Obtener nuevos resultados
        new_results = self.get_all_results(query, max_results, search_type)
        
        if not new_results:
            return {
                'message': 'No se encontraron resultados nuevos',
                'new_records': 0,
                'total_records': 0
            }
        
        # Cargar CSV existente si existe
        existing_df = pd.DataFrame()
        try:
            existing_df = pd.read_csv(csv_filename)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error leyendo CSV existente: {e}")
        
        # Convertir nuevos resultados a DataFrame
        new_df = pd.DataFrame(new_results)
        
        # Combinar con datos existentes
        if not existing_df.empty:
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        else:
            combined_df = new_df
        
        # Eliminar duplicados de manera más simple y segura
        initial_count = len(combined_df)
        
        # Crear columna auxiliar para deduplicación
        combined_df['dedup_key'] = combined_df['doi'].fillna('NO_DOI_' + combined_df['title'].astype(str))
        
        # Eliminar duplicados basándose en la clave
        combined_df = combined_df.drop_duplicates(subset=['dedup_key'], keep='last')
        
        # Remover columna auxiliar
        combined_df = combined_df.drop('dedup_key', axis=1)
        
        final_count = len(combined_df)
        duplicates_removed = initial_count - final_count
        
        # Guardar CSV actualizado
        combined_df.to_csv(csv_filename, index=False, encoding='utf-8')
        
        return {
            'message': f'Búsqueda completada y guardada en {csv_filename}',
            'new_records': len(new_results),
            'total_records': final_count,
            'duplicates_removed': duplicates_removed,
            'source': 'OpenAlex'
        }


def main():
    """Función principal para probar OpenAlex"""
    
    # Crear buscador
    searcher = OpenAlexSearcher()
    
    print("=== Buscador OpenAlex (Gratuito) ===")
    print("Búsqueda completa en título y abstract sin limitaciones")
    print()
    
    # Solicitar término de búsqueda
    query = input("Introduce el término de búsqueda: ").strip()
    
    if not query:
        print("❌ No se introdujo ningún término")
        return
    
    # Realizar búsqueda y guardar
    result = searcher.save_to_csv(
        query=query,
        csv_filename='openalex_results.csv',
        max_results=1000,  # Ajusta según necesites
        search_type='title_abstract'
    )
    
    print(f"\nOK: {result['message']}")
    print(f"Nuevos registros: {result['new_records']}")
    print(f"Total en CSV: {result['total_records']}")
    if 'duplicates_removed' in result:
        print(f"Duplicados eliminados: {result['duplicates_removed']}")
    print(f"Fuente: {result.get('source', 'OpenAlex')}")


if __name__ == "__main__":
    main()
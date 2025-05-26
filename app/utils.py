# app/utils.py

import pandas as pd
import psycopg2
from sqlalchemy.sql.elements import TextClause
from queries import coctel_queries, user_queries

def _get_connection():
    """
    Crea la conexión leyendo los secretos de Streamlit.
    """
    import streamlit as st
    secrets = st.secrets["postgres"]
    return psycopg2.connect(
        host     = secrets["host"],
        port     = secrets["port"],
        user     = secrets["user"],
        password = secrets["password"],
        dbname   = secrets["dbname"],
        sslmode  = secrets.get("sslmode", "require")
    )

def cargar_datos(query: TextClause) -> pd.DataFrame:
    """
    Ejecuta el query (SQLAlchemy TextClause) y devuelve un DataFrame.
    """
    conn = _get_connection()
    df = pd.read_sql_query(str(query), conn)
    conn.close()
    return df

# Mapa de categorías a sus diccionarios de queries
ALL_QUERIES = {
    "cocteles": coctel_queries.queries,
    "usuarios": user_queries.queries,
}

def get_query(category: str, table_name: str, mode: str = "read") -> pd.DataFrame:
    """
    category   : 'cocteles' o 'usuarios'
    table_name : nombre de la consulta en tu módulo queries (por ej. 'coctel_completo')
    mode       : generalmente 'read'
    """
    qdict = ALL_QUERIES.get(category)
    if not qdict:
        raise ValueError(f"Categoría '{category}' no encontrada.")
    entry = qdict.get(table_name)
    if not entry:
        raise ValueError(f"Query '{table_name}' no encontrado en '{category}'.")
    query = entry.get(mode)
    if query is None:
        raise ValueError(f"Modo '{mode}' no definido para '{table_name}'.")
    
    return cargar_datos(query)

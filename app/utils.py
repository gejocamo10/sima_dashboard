import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv
from sqlalchemy.sql.elements import TextClause
from queries import coctel_queries, user_queries

# Cargar variables de entorno
load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Función general para conectar y cargar un query
def cargar_datos(query: TextClause):
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME
    )
    df = pd.read_sql_query(str(query), conn)
    conn.close()
    return df

ALL_QUERIES = {
    "cocteles": coctel_queries.queries,
    "usuarios": user_queries.queries,
}

# Función general para obtener y ejecutar query
def get_query(category: str, table_name: str, mode: str = "read"):
    """
    category: 'cocteles', 'usuarios', etc.
    table_name: nombre del query (e.g., 'coctel_completo')
    mode: 'read', 'write', etc. (por defecto 'read')
    """
    query_dict = ALL_QUERIES.get(category)
    if not query_dict:
        raise ValueError(f"Categoría '{category}' no encontrada.")
    entry = query_dict.get(table_name)
    if not entry:
        raise ValueError(f"Query '{table_name}' no encontrado en categoría '{category}'.")
    query = entry.get(mode)
    if query is None:
        raise ValueError(f"Modo '{mode}' no definido para '{table_name}'.")
    return cargar_datos(query)


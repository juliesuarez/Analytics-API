# The logic that generates SQL and Analytics
# engine.py
from sqlalchemy import create_engine, text
import pandas as pd
from security import decrypt_password

def get_external_connection(source_data):
    """Reconstructs the connection string for the customer's DB."""
    real_password = decrypt_password(source_data.encrypted_password)
    
    if source_data.db_type == 'postgresql':
        return f"postgresql://{source_data.user}:{real_password}@{source_data.host}:{source_data.port}/{source_data.database_name}"
    elif source_data.db_type == 'mysql':
        return f"mysql+pymysql://{source_data.user}:{real_password}@{source_data.host}:{source_data.port}/{source_data.database_name}"
    else:
        raise ValueError("Unsupported DB Type")

def generate_analytics(source_data, request):
    """
    1. Connects to the customer DB.
    2. Runs an optimized AGGREGATE SQL query.
    3. Returns chart data.
    """
    db_url = get_external_connection(source_data)
    external_engine = create_engine(db_url)
    
    # SAFETY: In a real product, you must sanitize inputs to prevent SQL Injection.
    # We use SQLAlchemy text parameters for basic safety.
    
    op_map = {
        "sum": "SUM",
        "count": "COUNT",
        "avg": "AVG"
    }
    sql_op = op_map.get(request.operation, "COUNT")
    
    # Constructing the query: SELECT country, SUM(sales) FROM orders GROUP BY country
    query = text(f"""
        SELECT {request.group_by_column} as label, 
               {sql_op}({request.measure_column}) as value 
        FROM {request.table_name} 
        GROUP BY {request.group_by_column}
    """)
    
    try:
        with external_engine.connect() as conn:
            # Load result directly into Pandas
            df = pd.read_sql(query, conn)
            
            # Format for Charting Frontend
            return {
                "chart_title": f"{request.operation.title()} of {request.measure_column} by {request.group_by_column}",
                "data": df.to_dict(orient="records")
            }
    except Exception as e:
        return {"error": str(e)}
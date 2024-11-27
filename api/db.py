from sqlalchemy import create_engine
from sqlalchemy import text

engine = create_engine("mysql+mysqlconnector://root:0000@localhost:3306/bbdd_pythoneta")

def run_query(query, parameters=None):
    with engine.connect() as conn:
        result = conn.execute(text(query), parameters)
        conn.commit()
    return result

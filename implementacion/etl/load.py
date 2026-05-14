from sqlalchemy import text
from database.connection import engine

def load_data(df):

    with engine.begin() as conn:

        conn.execute(text('''
            CREATE TABLE IF NOT EXISTS importaciones (
                id SERIAL PRIMARY KEY,
                partida TEXT,
                cif NUMERIC,
                fob NUMERIC,
                flete NUMERIC,
                seguro NUMERIC,
                fecha TIMESTAMP
            );
        '''))

    df.to_sql(
        "importaciones",
        engine,
        if_exists="replace",
        index=False
    )

    print("Datos cargados correctamente")

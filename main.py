# Conexión a la base de datos
def conectar_db():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=MARTALB\SQLEXPRESS;'
        'DATABASE=PetlandDb;'
        'UID=sa;'
        'PWD=1234'
    )
    return conn

from articuloService import menu
menu()


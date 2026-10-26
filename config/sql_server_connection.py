import pyodbc

def create_connection():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=LAPTOP-42R9RHPJ\\SQLEXPRESS;"
        "DATABASE=ecommercesource;"
        "Trusted_Connection=yes;"
    )
    return conn 


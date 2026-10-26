import pytest
import pandas as pd
from config.sql_server_connection import create_connection
from config.postgresql_connection import create_postgresql_connection

@pytest.fixture
def source_data():
    conn = create_connection()
    cursor = conn.cursor()


    cursor.execute("""
            select customer_id,
            customer_name,
            email,
            country,
            updated_at
            from source_data.customers
""")

    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]

    return pd.DataFrame.from_records(
        rows,
        columns=columns,
    )


@pytest.fixture
def target_data():

    conn = create_postgresql_connection()
    cursor = conn.cursor()

    cursor.execute("""
        select 
        customer_id,
        customer_name,
        email,
        country,
        updated_at
        from target_data.customers
        """)

    rows = cursor.fetchall()

    columns = [column[0] for column in cursor.description]

    return pd.DataFrame.from_records(
        rows,
        columns=columns
    )

    cursor.close()
    conn.close()
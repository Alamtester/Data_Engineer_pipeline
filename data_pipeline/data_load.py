from config.postgresql_connection import create_postgresql_connection


def customer_data_load(data):

    conn = create_postgresql_connection()
    
    cursor = conn.cursor()

   # cursor.execute('select current_database();')
   # database_name = cursor.fetchone()[0]

    #print(f'Python is connected to database: {database_name}')

    insert_query = """
            INSERT INTO target_data.customers(
            customer_id,
            customer_name ,
            email,
            country,
            updated_at)
            VALUES (%s,%s,%s,%s,%s)
                    """

    cursor.executemany(insert_query,data)

    records_loaded = cursor.rowcount

    conn.commit()
    
    print(f"Successfully loaded {records_loaded} records")
    return records_loaded


    cursor.close()
    conn.close()
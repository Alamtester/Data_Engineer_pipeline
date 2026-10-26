from config.sql_server_connection import create_connection

def customer_data_extraction():
    conn = create_connection()

    cursor = conn.cursor() 

    schemaname = 'source_data'
    tablename = 'customers' 

    extraction_query = f'select * from {schemaname}.{tablename}'

    cursor.execute(extraction_query)

    data = cursor.fetchall()
    print(f'Total Records are extracted: {len(data)}')
    return data





from config.sql_server_connection import create_connection


def customer_data_extraction(last_watermark=None):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        if last_watermark is None:
            query = """
                SELECT customer_id, customer_name, email, country, updated_at
                FROM source_data.customers
            """
            cursor.execute(query)
        else:
            query = """
                SELECT customer_id, customer_name, email, country, updated_at
                FROM source_data.customers
                WHERE updated_at >= ?
            """
            cursor.execute(query, (last_watermark,))

        data = cursor.fetchall()
        print(f"Successfully extracted {len(data)} records")
        return data

    except Exception as exc:
        print(f"Error extracting data: {exc}")
        raise

    finally:
        cursor.close()
        conn.close()

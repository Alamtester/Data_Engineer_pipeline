from config.postgresql_connection import create_postgresql_connection


def save_pipeline_audit(
        pipeline_name,
        start_time,
        end_time,
        records_extracted,
        records_transformed,
        records_load,
        status
):

    conn = create_postgresql_connection()

    cursor = conn.cursor()

    insert_query = """
            insert into pipeline_audit(
            pipeline_name,
            start_time,
            end_time,
            records_extracted,
            records_transformed,
            records_load,
            status
            )
            values(%s,%s,%s,%s,%s,%s,%s)
            """

    cursor.execute(insert_query,(
        pipeline_name,
        start_time,
        end_time,
        records_extracted,
        records_transformed,
        records_load,
        status
    ))

    conn.commit()

    print("Pipeline audit record saved successfully")

    cursor.close()
    conn.close()

    
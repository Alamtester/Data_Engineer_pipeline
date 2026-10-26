
from config.postgresql_connection import create_postgresql_connection


def create_pipeline_control_table():
    """Create the pipeline control table if it does not exist."""

    conn = create_postgresql_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS public.pipeline_control (
                pipeline_name VARCHAR(100) PRIMARY KEY,
                last_successful_watermark TIMESTAMP NULL,
                updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        print("Pipeline control table is ready.")

    except Exception as exc:
        conn.rollback()
        print(f"Error creating pipeline control table: {exc}")
        raise

    finally:
        cursor.close()
        conn.close()


def get_last_watermark(pipeline_name):
    """
    Return the last saved watermark.
    Return None on the first run when no watermark exists.
    """

    create_pipeline_control_table()

    conn = create_postgresql_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT last_successful_watermark
            FROM public.pipeline_control
            WHERE pipeline_name = %s;
        """, (pipeline_name,))

        result = cursor.fetchone()

        if result is None:
            return None

        return result[0]

    finally:
        cursor.close()
        conn.close()


def save_watermark(pipeline_name, watermark):
    """Insert or update the watermark after successful processing."""

    create_pipeline_control_table()

    conn = create_postgresql_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO public.pipeline_control (
                pipeline_name,
                last_successful_watermark,
                updated_at
            )
            VALUES (%s, %s, CURRENT_TIMESTAMP)
            ON CONFLICT (pipeline_name)
            DO UPDATE SET
                last_successful_watermark =
                    EXCLUDED.last_successful_watermark,
                updated_at = CURRENT_TIMESTAMP;
        """, (pipeline_name, watermark))

        conn.commit()
        print(f"Watermark saved successfully: {watermark}")

    except Exception as exc:
        conn.rollback()
        print(f"Error saving watermark: {exc}")
        raise

    finally:
        cursor.close()
        conn.close()

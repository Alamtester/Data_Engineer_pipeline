
from datetime import datetime

from data_pipeline.data_extraction import customer_data_extraction
from data_pipeline.data_transformation import data_transformation
from data_pipeline.data_load import customer_data_load
from data_pipeline.pipeline_control import (
    get_last_watermark,
    save_watermark,
)
from data_pipeline.pipeline_audit import save_pipeline_audit
from data_pipeline.pipeline_report import generate_pipeline_report


def main():
    pipeline_name = "Customer Data Pipeline"
    start_time = datetime.now()
    run_id = start_time.strftime("%Y%m%d_%H%M%S_%f")

    status = "FAILED"
    current_stage = "Initialization"
    failed_stage = ""
    error_message = ""

    records_extracted = 0
    records_transformed = 0
    records_loaded = 0

    last_watermark = None
    new_watermark = None

    try:
        # 1. Retrieve the previously saved watermark
        current_stage = "Read watermark"
        last_watermark = get_last_watermark(pipeline_name)
        print(f"Previous watermark: {last_watermark}")

        # 2. Extract all rows on the first run,
        #    or changed rows on subsequent runs
        current_stage = "Extract data"
        data = customer_data_extraction(last_watermark)
        records_extracted = len(data)
        print(f"Records extracted: {records_extracted}")

        # 3. Transform the extracted rows
        current_stage = "Transform data"
        transformed_data = data_transformation(data)
        records_transformed = len(transformed_data)
        print(f"Records transformed: {records_transformed}")

        # 4. Load/upsert the rows into PostgreSQL
        current_stage = "Load data"
        records_loaded = customer_data_load(transformed_data)
        print(f"Records loaded/processed: {records_loaded}")

        # 5. Advance the watermark only after load succeeds
        current_stage = "Save watermark"

        valid_timestamps = [
            row[4] for row in data if row[4] is not None
        ]

        if valid_timestamps:
            new_watermark = max(valid_timestamps)
            save_watermark(pipeline_name, new_watermark)
        else:
            print("No new records; watermark unchanged.")

        # 6. Record successful execution
        current_stage = "Write success audit"
        end_time = datetime.now()

        save_pipeline_audit(
            pipeline_name,
            start_time,
            end_time,
            records_extracted,
            records_transformed,
            records_loaded,
            status
        )

        status = "SUCCESS"
        print("Data Pipeline Completed Successfully")

    except Exception as exc:
        failed_stage = current_stage
        error_message = f"{type(exc).__name__}: {exc}"

        print(f"Pipeline failed during: {failed_stage}")
        print(f"Error: {error_message}")

    finally:
        end_time = datetime.now()
        duration_seconds = round(
            (end_time - start_time).total_seconds(), 2
        )

        report_data = {
            "run_id": run_id,
            "pipeline_name": pipeline_name,
            "status": status,
            "start_time": start_time.isoformat(sep=" ", timespec="seconds"),
            "end_time": end_time.isoformat(sep=" ", timespec="seconds"),
            "duration_seconds": duration_seconds,
            "records_extracted": records_extracted,
            "records_transformed": records_transformed,
            "records_loaded": records_loaded,
            "previous_watermark": last_watermark,
            "new_watermark": new_watermark,
            "failed_stage": failed_stage,
            "error_message": error_message,
        }

        try:
            result = generate_pipeline_report(report_data)

            for path in result["created_files"]:
                print(f"Report generated: {path}")

            for warning in result["errors"]:
                print(f"Reporting warning: {warning}")

        except Exception as report_exc:
            print(f"Could not generate reports: {report_exc}")

        print(f"Final pipeline status: {status}")
        print(f"Duration: {duration_seconds} seconds")


if __name__ == "__main__":
    main()






























# from data_pipeline.data_extraction import customer_data_extraction
# from data_pipeline.data_transformation import data_transformation
# from data_pipeline.data_load import customer_data_load
# from data_pipeline.pipeline_audit import save_pipeline_audit
# from datetime import datetime 


# def main():

#     pipeline_name = "Customer Data Pipeline"

#     start_time = datetime.now()

#     print("Starting Data Pipeline")

#     data = customer_data_extraction()
#     records_extracted = len(data)

#     transformed_data = data_transformation(data)
#     records_transformed = len(transformed_data)

#     customer_loaded = customer_data_load(transformed_data)
#     records_load = customer_loaded

#     end_time = datetime.now()

#     save_pipeline_audit(
#             pipeline_name,
#             start_time,
#             end_time,
#             records_extracted,
#             records_transformed,
#             records_load,
#             "SUCCESS"

#     )

#     print("Data Pipeline Completed Successfully")

# if __name__ == "__main__":
#     main()



# from datetime import datetime

# from data_pipeline.data_extraction import customer_data_extraction
# from data_pipeline.data_transformation import data_transformation
# from data_pipeline.data_load import customer_data_load
# from data_pipeline.pipeline_control import (
#     get_last_watermark,
#     save_watermark,
# )
# from data_pipeline.pipeline_audit import save_pipeline_audit
# from data_pipeline.pipeline_report import generate_pipeline_report


# def main():
#     pipeline_name = "Customer Data Pipeline"

#     start_time = datetime.now()
#     run_id = start_time.strftime("%Y%m%d_%H%M%S_%f")

#     status = "FAILED"
#     current_stage = "Initialization"
#     failed_stage = ""
#     error_message = ""

#     records_extracted = 0
#     records_transformed = 0
#     records_loaded = 0

#     last_watermark = None
#     new_watermark = None

#     print("=" * 50)
#     print("Starting Customer Data Pipeline")
#     print(f"Run ID: {run_id}")
#     print("=" * 50)

#     try:
#         # 1. Read the previous watermark
#         current_stage = "Read watermark"
#         last_watermark = get_last_watermark(pipeline_name)

#         print(f"Previous watermark: {last_watermark}")

#         # 2. Extract source data
#         current_stage = "Extract data"
#         data = customer_data_extraction(last_watermark)
#         records_extracted = len(data)

#         print(f"Records extracted: {records_extracted}")

#         # 3. Transform data
#         current_stage = "Transform data"
#         transformed_data = data_transformation(data)
#         records_transformed = len(transformed_data)

#         print(f"Records transformed: {records_transformed}")

#         # 4. Load data into PostgreSQL
#         current_stage = "Load data"
#         records_loaded = customer_data_load(transformed_data)

#         print(f"Records loaded/processed: {records_loaded}")

#         # 5. Save watermark only when there is source data
#         current_stage = "Save watermark"

#         if data:
#             new_watermark = max(row[4] for row in data)
#             save_watermark(pipeline_name, new_watermark)

#         # 6. Write successful-run audit
#         current_stage = "Write success audit"
#         end_time = datetime.now()

#         save_pipeline_audit(
#             pipeline_name,
#             start_time,
#             end_time,
#             records_extracted,
#             records_transformed,
#             records_loaded,
#             status
#         )

#         status = "SUCCESS"
#         print("Data Pipeline Completed Successfully")

#     except Exception as exc:
#         failed_stage = current_stage
#         error_message = f"{type(exc).__name__}: {exc}"

#         print(f"Pipeline failed during: {failed_stage}")
#         print(f"Error: {error_message}")

#     finally:
#         end_time = datetime.now()
#         duration_seconds = round(
#             (end_time - start_time).total_seconds(), 2
#         )

#         # 7. Generate CSV and HTML reports after every run
#         report_data = {
#             "run_id": run_id,
#             "pipeline_name": pipeline_name,
#             "status": status,
#             "start_time": start_time.isoformat(sep=" ", timespec="seconds"),
#             "end_time": end_time.isoformat(sep=" ", timespec="seconds"),
#             "duration_seconds": duration_seconds,
#             "records_extracted": records_extracted,
#             "records_transformed": records_transformed,
#             "records_loaded": records_loaded,
#             "previous_watermark": last_watermark,
#             "new_watermark": new_watermark,
#             "failed_stage": failed_stage,
#             "error_message": error_message,
#         }

#         try:
#             result = generate_pipeline_report(report_data)

#             for path in result["created_files"]:
#                 print(f"Report generated: {path}")

#             for report_error in result["errors"]:
#                 print(f"Reporting warning: {report_error}")

#         except Exception as report_exc:
#             # A report failure should not hide the pipeline result.
#             print(f"Could not generate reports: {report_exc}")

#         print("=" * 50)
#         print(f"Final pipeline status: {status}")
#         print(f"Duration: {duration_seconds} seconds")
#         print("=" * 50)


# if __name__ == "__main__":
#     main()



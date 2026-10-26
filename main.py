from data_pipeline.data_extraction import customer_data_extraction
from data_pipeline.data_transformation import data_transformation
from data_pipeline.data_load import customer_data_load
from data_pipeline.pipeline_audit import save_pipeline_audit
from datetime import datetime


def main():

    pipeline_name = "Customer Data Pipeline"

    start_time = datetime.now()

    print("Starting Data Pipeline")

    data = customer_data_extraction()
    records_extracted = len(data)

    transformed_data = data_transformation(data)
    records_transformed = len(transformed_data)

    customer_loaded = customer_data_load(transformed_data)
    records_load = customer_loaded

    end_time = datetime.now()

    save_pipeline_audit(
            pipeline_name,
            start_time,
            end_time,
            records_extracted,
            records_transformed,
            records_load,
            "SUCCESS"

    )

    print("Data Pipeline Completed Successfully")

if __name__ == "__main__":
    main()


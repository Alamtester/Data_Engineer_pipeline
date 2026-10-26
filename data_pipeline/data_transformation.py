from data_pipeline.data_extraction import customer_data_extraction



def data_transformation(data):

    transformed_data =[]

    for row in data:

        customer_id = row[0]
        customer_name = row[1]
        email = row[2]
        country = row[3]
        updated_at = row[4]


        customer_name = customer_name.strip()


        email = email.strip()

        country = country.strip()

        transformed_row = (
            customer_id,
            customer_name,
            email,
            country,
            updated_at
        )

        transformed_data.append(transformed_row)

    print(f"Transformed data:{len(transformed_data[0])}")


    return transformed_data



    
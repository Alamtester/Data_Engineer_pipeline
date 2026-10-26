import pandas as pd


def test_source_and_target_record_counts(source_data, target_data):

    assert len(source_data) == len(target_data), (
        f"Source count: {len(source_data)}, "
        f"Target count: {len(target_data)}"
    )


def test_source_has_no_duplicate_customer_ids(source_data):

    duplicate_ids = source_data.loc[
        source_data["customer_id"].duplicated(),
        "customer_id"
    ]

    assert duplicate_ids.empty, (
        f"Duplicate IDs in source: {duplicate_ids.tolist()[:10]}"
    )


def test_target_has_no_duplicate_customer_ids(target_data):

    duplicate_ids = target_data.loc[
        target_data["customer_id"].duplicated(),
        "customer_id"
    ]

    assert duplicate_ids.empty, (
        f"Duplicate IDs in target: {duplicate_ids.tolist()[:10]}"
    )


def test_no_source_customers_are_missing_from_target(
    source_data,
    target_data
):

    missing_ids = set(source_data["customer_id"]) - set(
        target_data["customer_id"]
    )

    assert not missing_ids, (
        f"Customer IDs missing from target: {list(missing_ids)[:10]}"
    )


def test_customer_transformation_rules(source_data, target_data):

    expected = source_data.copy()

    # Apply the same documented transformation rules
    expected["customer_name"] = (
        expected["customer_name"].str.strip()
    )

    expected["email"] = (
        expected["email"].str.strip().str.lower()
    )

    expected["country"] = (
        expected["country"].str.strip().str.title()
    )

    # Compare by customer_id rather than row order
    expected = expected.sort_values("customer_id").reset_index(drop=True)

    actual = target_data.sort_values("customer_id").reset_index(drop=True)

    columns_to_compare = [
        "customer_id",
        "customer_name",
        "email",
        "country"
    ]

    pd.testing.assert_frame_equal(
        expected[columns_to_compare],
        actual[columns_to_compare],
        check_dtype=False
    )

def test_updated_at_matches_source(source_data, target_data):

        source = source_data[
        ["customer_id", "updated_at"]
    ].copy()

        target = target_data[
        ["customer_id", "updated_at"]
    ].copy()

    # Normalize timestamps for comparison
        source["updated_at"] = pd.to_datetime(
        source["updated_at"], utc=True
    )

        target["updated_at"] = pd.to_datetime(
        target["updated_at"], utc=True
    )

        comparison = source.merge(
        target,
        on="customer_id",
        how="inner",
        suffixes=("_source", "_target"),
        validate="one_to_one"
    )

        mismatches = comparison[
        comparison["updated_at_source"]
        != comparison["updated_at_target"]
    ]

        assert mismatches.empty, (
        f"Timestamp mismatches:\n{mismatches.head(10)}"
    )
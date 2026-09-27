import pandera.pandas as pa

ALLOWED_CITIES = ["Stockholm", "Göteborg", "Malmö", "Uppsala"]


schema = pa.DataFrameSchema(
    {
        "customer_id": pa.Column(int, unique=True),
        "age": pa.Column(
            int,
            pa.Check.in_range(18, 100)
        ),
        "income": pa.Column(
            float,
            nullable=False
        ),
        "city": pa.Column(
            str,
            pa.Check.isin(ALLOWED_CITIES)
        ),
        "active": pa.Column(bool),
    },
    strict=True
)


def validate_with_pandera(df):
    """
    Validerar datan med Pandera.
    True returneras om datan är godkänd, annars False.
    """
    try:
        schema.validate(df, lazy=True)
        print("Pandera: Datan klarade alla kontroller.")
        return True

    except pa.errors.SchemaErrors as error:
        print("Pandera hittade fel i datan:")
        print(error.failure_cases.to_string(index=False))
        return False

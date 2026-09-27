import pandas as pd

ALLOWED_CITIES = ["Stockholm", "Göteborg", "Malmö", "Uppsala"]


def validate_with_pandas(df):
    """
    Validerar datan med vanliga Pandas-kontroller.
    Funktionen returnerar en lista med de fel som hittas.
    """
    errors = []

    # Kontroll 1: rätt kolumner ska finnas
    required_columns = ["customer_id", "age", "income", "city", "active"]

    for column in required_columns:
        if column not in df.columns:
            errors.append(f"Kolumnen {column} saknas.")

    # Om en viktig kolumn saknas avslutas kontrollerna här.
    if errors:
        return errors

    # Kontroll 2: customer_id ska vara unik
    if df["customer_id"].duplicated().any():
        duplicate_ids = df.loc[
            df["customer_id"].duplicated(keep=False),
            "customer_id"
        ].tolist()
        errors.append(f"Dubbletter i customer_id: {duplicate_ids}")

    # Kontroll 3: age ska vara numerisk
    if not pd.api.types.is_numeric_dtype(df["age"]):
        errors.append("Kolumnen age ska vara numerisk.")
    else:
        invalid_age = df.loc[
            ~df["age"].between(18, 100),
            ["customer_id", "age"]
        ]

        if not invalid_age.empty:
            errors.append(
                "Ålder utanför intervallet 18-100: "
                + str(invalid_age.to_dict(orient="records"))
            )

    # Kontroll 4: income ska vara numerisk och får inte saknas
    if not pd.api.types.is_numeric_dtype(df["income"]):
        errors.append("Kolumnen income ska vara numerisk.")

    if df["income"].isna().any():
        missing_income = df.loc[
            df["income"].isna(),
            "customer_id"
        ].tolist()
        errors.append(
            f"Saknat income för customer_id: {missing_income}"
        )

    # Kontroll 5: city ska innehålla ett tillåtet värde
    invalid_city = df.loc[
        ~df["city"].isin(ALLOWED_CITIES),
        ["customer_id", "city"]
    ]

    if not invalid_city.empty:
        errors.append(
            "Ogiltig stad: "
            + str(invalid_city.to_dict(orient="records"))
        )

    # Kontroll 6: active ska vara boolesk
    if not pd.api.types.is_bool_dtype(df["active"]):
        errors.append(
            "Kolumnen active har fel datatyp. "
            "Förväntad datatyp är bool."
        )

    return errors

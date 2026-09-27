from pathlib import Path

import pandas as pd

from src.pandas_validation import validate_with_pandas
from src.pandera_validation import validate_with_pandera


DATA_FILE = Path(__file__).parent / "data" / "testdata.csv"


def main():
    # Läs in CSV-filen.
    df = pd.read_csv(DATA_FILE)

    print("=" * 60)
    print("TESTDATA")
    print("=" * 60)
    print(df)

    print("\n" + "=" * 60)
    print("VALIDERING MED PANDAS")
    print("=" * 60)

    pandas_errors = validate_with_pandas(df)

    if pandas_errors:
        for error in pandas_errors:
            print(f"- {error}")
    else:
        print("Pandas: Datan klarade alla kontroller.")

    print("\n" + "=" * 60)
    print("VALIDERING MED PANDERA")
    print("=" * 60)

    validate_with_pandera(df)

    print("\n" + "=" * 60)
    print("KORT JÄMFÖRELSE")
    print("=" * 60)
    print(
        "Pandas kräver att varje kontroll skrivs separat. "
        "Med Pandera samlas reglerna i ett schema."
    )


if __name__ == "__main__":
    main()

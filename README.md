# Datavalidering med Pandas och Pandera

## Om projektet

Det här projektet är min individuella Pythonfördjupning inom datavalidering.

Syftet är att undersöka hur datavalidering kan göras med vanlig Pandas-kod och jämföra det med biblioteket Pandera.

Projektet är medvetet avgränsat till ett mindre dataset och några vanliga kontroller av datakvalitet.

## Vad programmet kontrollerar

Programmet kontrollerar:

- att rätt kolumner finns,
- att `customer_id` inte innehåller dubbletter,
- att `age` är numerisk och ligger mellan 18 och 100,
- att `income` är numerisk och inte saknas,
- att `city` innehåller ett tillåtet värde,
- att `active` har boolesk datatyp.

Samma testdata valideras först med Pandas och sedan med Pandera.

## Projektstruktur

```text
datavalidering-pandas-pandera/
├── data/
│   └── testdata.csv
├── src/
│   ├── __init__.py
│   ├── pandas_validation.py
│   └── pandera_validation.py
├── report/
│   └── rapport.md
├── presentation/
│   ├── manus.md
│   └── Manus till Python uppgift 2.pdf
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

## Data

Datasetet `data/testdata.csv` är syntetiskt, innehåller 150 rader och är skapat specifikt för det här projektet.

Det innehåller inga riktiga personuppgifter.

Jag har medvetet lagt in några fel i datan för att kunna demonstrera valideringen. Exempel är:

- en dubblett i `customer_id`,
- två åldrar utanför det tillåtna intervallet,
- ett saknat värde i `income`,
- en stad som inte är tillåten,
- ett felaktigt värde i `active`.

Värdet `"yes"` i kolumnen `active` är medvetet inlagt som felaktig testdata, eftersom kolumnen enligt valideringsreglerna endast ska innehålla de booleska värdena `True` eller `False`.

## Installation

Projektet kräver Python samt biblioteken Pandas och Pandera.

Öppna projektmappen i Visual Studio Code och öppna terminalen.

Skapa en virtuell miljö:

```bash
python -m venv .venv
```

Aktivera miljön i Git Bash:

```bash
source .venv/Scripts/activate
```

Eller i PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Installera beroenden:

```bash
pip install -r requirements.txt
```

## Kör projektet

Kör följande kommando från projektmappen:

```bash
python main.py
```

Programmet läser in testdatan och visar sedan vilka fel som hittas med Pandas och Pandera.

## Beroenden

Projektet använder:

- Pandas
- Pandera

Beroendena finns även i `requirements.txt`.

## Kort jämförelse

Med Pandas skrivs varje kontroll separat med exempelvis `duplicated()`, `between()`, `isna()` och `isin()`.

Med Pandera samlas reglerna i ett schema som sedan används för att validera hela DataFrame-objektet.

## Rapport

Den skriftliga rapporten finns i:

```text
report/rapport.md
```

## Presentation

Ett manus med förberedda frågor och svar finns i mappen `presentation/`.
PDF-filen är tänkt som stöd inför den muntliga presentationen och behöver inte användas som en del av själva programkörningen.

## Källor

De viktigaste källorna som används i projektet är:

- Pandera Documentation: https://pandera.readthedocs.io/
- Pandas Documentation: https://pandas.pydata.org/docs/
- Python Documentation: https://docs.python.org/3/

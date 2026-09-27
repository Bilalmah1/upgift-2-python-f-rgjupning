# Datavalidering med Pandas och Pandera

## Syfte

Syftet med det här arbetet är att fördjupa mig inom datavalidering i Python. Jag ville undersöka hur datavalidering kan göras med biblioteket Pandera och jämföra det med att göra samma typ av kontroller direkt i Pandas.

Jag har tidigare använt Pandas för att läsa in, rensa och analysera data. Därför ville jag välja ett område som fortfarande har tydlig koppling till det jag redan kan, men där jag samtidigt får lära mig ett nytt Pythonbibliotek. Min frågeställning blev därför vad Pandera tillför jämfört med att bara använda vanliga Pandas-kontroller.

Arbetet är avgränsat till ett mindre syntetiskt dataset och några vanliga regler för datakvalitet. Jag testar bland annat dubbletter, saknade värden, datatyper, tillåtna kategorier och värdeintervall. Jag bygger inte någon maskininlärningsmodell eller ett större produktionssystem.

## Området och dess relevans

Datavalidering betyder att man kontrollerar att data följer vissa regler innan den används vidare. Ett dataset kan till exempel innehålla saknade värden, fel datatyp, dubbletter eller värden som inte är rimliga. Om sådana fel inte upptäcks kan de påverka en analys eller en modell senare.

Det här är relevant för Data Science eftersom mycket arbete börjar med att förstå och kontrollera data. En Data Scientist eller dataanalytiker behöver kunna avgöra om datan går att lita på innan den används för rapportering, visualisering eller maskininlärning.

I vanliga Pandas går det att göra många datakontroller. Exempelvis kan `isna()` användas för att hitta saknade värden, `duplicated()` för dubbletter, `between()` för intervall och `isin()` för att kontrollera tillåtna värden. Nackdelen är att man själv behöver skriva varje regel och bestämma hur felen ska hanteras.

Pandera är ett bibliotek som är gjort för datavalidering. I Pandera kan man definiera ett schema som beskriver hur ett DataFrame-objekt ska se ut. Där kan man ange vilka kolumner som ska finnas, vilken datatyp de ska ha och olika regler för deras värden.

## Viktiga begrepp

### Datakvalitet

Datakvalitet handlar om hur användbar och pålitlig data är. I mitt projekt tittar jag främst på om värden saknas, om samma ID förekommer flera gånger, om värden ligger inom ett rimligt intervall och om rätt datatyp används.

### Datavalidering

Datavalidering innebär att kontrollera data mot bestämda regler. Om en regel inte uppfylls ska programmet kunna visa att något är fel.

### DataFrame

En DataFrame är Pandas tabellstruktur med rader och kolumner. CSV-filen i projektet läses in som en DataFrame och skickas sedan till båda valideringslösningarna.

### Schema

Ett schema beskriver hur data förväntas vara uppbyggd. I Pandera använder jag `DataFrameSchema`. I schemat anger jag kolumnerna och vilka regler som gäller för varje kolumn.

### Check

En check är en kontrollregel i Pandera. Jag använder bland annat `pa.Check.in_range()` för att kontrollera att ålder ligger mellan 18 och 100 och `pa.Check.isin()` för att kontrollera att stad finns bland tillåtna värden.

### Lazy validation

När jag kör Pandera använder jag `lazy=True`. Det gör att Pandera försöker samla flera fel innan valideringen avbryts. Det passar bra i det här projektet eftersom testdatan innehåller flera medvetna fel och jag vill kunna se flera av dem i samma körning.

## Genomförande

Jag började med att skapa ett litet syntetiskt dataset i CSV-format. Jag valde syntetisk data eftersom jag inte behövde någon extern tjänst eller riktiga personuppgifter för att visa hur datavalidering fungerar.

Datasetet har fem kolumner:

- `customer_id`
- `age`
- `income`
- `city`
- `active`

Jag lade medvetet in några fel i datasetet för att kunna testa valideringen. Det finns en dubblett i `customer_id`, två åldrar utanför intervallet 18 till 100, ett saknat värde i `income`, staden `Västerås` som inte finns bland de tillåtna städerna och värdet `yes` i `active` i stället för ett booleskt värde. Värdet `yes` är medvetet inlagt som felaktig testdata eftersom kolumnen `active` enligt valideringsreglerna endast ska innehålla `True` eller `False`.

### Validering med Pandas

I filen `pandas_validation.py` skapade jag funktionen `validate_with_pandas`. Funktionen tar emot en DataFrame och skapar först en tom lista som heter `errors`.

Varje kontroll görs sedan separat. Om programmet hittar ett problem läggs en text till i listan.

För dubbletter använder jag:

```python
df["customer_id"].duplicated().any()
```

För ålder använder jag:

```python
df["age"].between(18, 100)
```

För saknade värden använder jag:

```python
df["income"].isna()
```

För städer använder jag:

```python
df["city"].isin(ALLOWED_CITIES)
```

Till sist returnerar funktionen listan med de fel som hittades. Fördelen med den här lösningen är att den är enkel att läsa när man redan känner till Pandas. Samtidigt blir det ganska mycket egen kod eftersom varje regel måste skrivas separat.

### Validering med Pandera

I filen `pandera_validation.py` definierade jag i stället ett schema.

Exempelvis ser regeln för ålder ut så här:

```python
"age": pa.Column(
    int,
    pa.Check.in_range(18, 100)
)
```

Det betyder att kolumnen ska innehålla heltal och att värdena ska ligga mellan 18 och 100.

För `customer_id` använder jag `unique=True`, för `income` använder jag `nullable=False` och för `city` använder jag `pa.Check.isin(ALLOWED_CITIES)`.

Sedan validerar jag hela DataFrame-objektet med:

```python
schema.validate(df, lazy=True)
```

Om datan bryter mot reglerna fångar jag `SchemaErrors` och skriver ut de fel som Pandera hittade.

### Programmets startpunkt

`main.py` är projektets startpunkt. Där läses CSV-filen in med Pandas. Sedan skickas samma DataFrame först till Pandas-funktionen och sedan till Pandera-funktionen.

Jag valde detta upplägg för att göra jämförelsen tydlig. Båda metoderna får exakt samma data och kontrollerar i stort sett samma saker.

## Resultat

Lösningen visar att både Pandas och Pandera kan användas för att hitta problem i ett dataset.

Med Pandas hittas bland annat:

- dubbletten i `customer_id`,
- åldrar som ligger utanför 18 till 100,
- det saknade värdet i `income`,
- den ogiltiga staden,
- fel datatyp i `active`.

Pandera kontrollerar motsvarande regler genom schemat. Eftersom jag använder `lazy=True` kan flera valideringsfel samlas och visas vid samma körning.

Det tydligaste resultatet för mig var skillnaden i hur reglerna organiseras. Med Pandas skriver jag själv all kontrollkod och bestämmer hur varje fel ska sparas och visas. Med Pandera kan flera regler samlas i ett schema, vilket gör att själva reglerna blir samlade på ett ställe.

Pandas-lösningen är fortfarande fullt fungerande och kan vara tillräcklig i ett litet projekt. Pandera blir mer tydligt när man vill beskriva vilka krav ett dataset ska uppfylla och kontrollera dessa krav på samma sätt flera gånger.

## Begränsningar och möjliga förbättringar

Projektet är medvetet litet. Datasetet är syntetiskt och innehåller 150 rader. Därför säger projektet inget om prestanda på stora dataset.

Jag testar också bara några vanliga typer av regler. Det finns fler saker som skulle kunna valideras, till exempel datumformat, textmönster, beroenden mellan flera kolumner eller mer avancerade regler.

En annan begränsning är att lösningen bara skriver ut fel. Den försöker inte automatiskt rätta felaktig data. Det är ett medvetet val eftersom syftet är att undersöka validering och inte bygga ett komplett datarensningssystem.

Om jag fortsatte projektet skulle ett naturligt nästa steg vara att testa Pandera på ett större verkligt dataset. Jag skulle också kunna undersöka hur ett schema kan återanvändas i ett dataflöde där nya CSV-filer läses in regelbundet.

## Koppling till yrkesrollen

Jag tycker att området har tydlig koppling till arbete inom Data Science och dataanalys. Innan data används till analys behöver man veta att den har rätt struktur och rimliga värden.

I ett företag kan samma typ av data komma in varje dag eller varje vecka. Då kan en valideringslösning användas för att upptäcka om en ny fil plötsligt saknar en kolumn, innehåller fel datatyp eller har värden som inte borde förekomma.

Det kan minska risken att felaktig data används i rapporter eller modeller. För en dataanalytiker kan det också göra datakvalitetskontroller mer konsekventa.

## Källor

Jag har främst använt officiell dokumentation för att förstå metoderna och biblioteket.

- Pandera Documentation, DataFrame Schemas: https://pandera.readthedocs.io/en/latest/dataframe_schemas.html
- Pandera Documentation, DataFrameSchema: https://pandera.readthedocs.io/en/latest/reference/generated/pandera.api.pandas.container.DataFrameSchema.html
- Pandas Documentation: https://pandas.pydata.org/docs/
- Python Documentation: https://docs.python.org/3/

## Självreflektion

### 1. Vad lärde du dig som du inte kunde innan?

Jag lärde mig hur Pandera kan användas för att skapa ett schema för en Pandas DataFrame. Tidigare hade jag främst gjort kontroller direkt med Pandas. Nu förstår jag bättre skillnaden mellan att skriva separata kontroller och att samla regler i ett schema.

### 2. Vad var svårast att förstå eller genomföra?

Det svåraste var i början att förstå hur reglerna i ett Pandera-schema hänger ihop med Pandas datatyper och hur Pandera visar valideringsfel. När jag delade upp det kolumn för kolumn blev det lättare.

### 3. Vilket tekniskt val är du mest nöjd med och varför?

Jag är mest nöjd med att jag använder samma testdata för båda metoderna. Det gör jämförelsen mer rättvis och lättare att förstå eftersom skillnaden ligger i hur valideringen görs och inte i vilken data som används.

### 4. Vad hade du gjort annorlunda om du började om?

Jag hade börjat med ännu färre regler och testat dem en i taget innan jag lade till resten. Det hade gjort felsökningen enklare i början.

### 5. Vad skulle vara ett naturligt nästa steg om du fortsatte arbetet?

Nästa steg skulle vara att använda ett större dataset och testa fler typer av regler. Jag skulle också kunna testa hur valideringen kan användas automatiskt när nya filer kommer in.

### 6. Vilket betyg tycker du själv att arbetet motsvarar – G eller VG?

Jag tycker att arbetet motsvarar G.

### 7. Motivera din bedömning genom att koppla till kraven för G och VG.

Jag har valt ett relevant och avgränsat område inom Python och Data Science. Jag har använt ett nytt bibliotek, Pandera, och byggt en fungerande mindre lösning där jag jämför det med Pandas. Projektet har tydlig struktur, README, beroenden och information om datan. Jag kan också förklara de viktigaste delarna av koden och vad ett schema och valideringsregler gör.

Jag bedömer arbetet som G eftersom jag har fokuserat på att uppfylla grundkraven på ett tydligt sätt och inte försökt göra projektet mer avancerat än nödvändigt.

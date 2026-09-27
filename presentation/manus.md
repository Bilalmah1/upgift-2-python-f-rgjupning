# Manus till Python uppgift 2

## Datavalidering med Pandas och Pandera

### Inledning

Hej. I min Pythonfördjupning har jag valt att arbeta med datavalidering.

Jag ville undersöka hur man kan kontrollera datakvalitet med vanlig Pandas-kod och sedan jämföra det med biblioteket Pandera. Jag har arbetat med Pandas tidigare, men Pandera var nytt för mig.

Datavalidering är relevant inom Data Science eftersom data kan innehålla fel som påverkar analyser, rapporter eller modeller.

### Vad jag byggde

Jag skapade ett syntetiskt dataset med 150 rader. Datan innehåller kolumnerna `customer_id`, `age`, `income`, `city` och `active`.

De flesta raderna är korrekta, men jag lade medvetet in några fel för att kunna testa valideringen:

- en dubblett i `customer_id`,
- en ålder på 17,
- en ålder på 101,
- ett saknat värde i `income`,
- staden `Västerås`, som inte finns bland de tillåtna städerna,
- värdet `yes` i `active`, där endast `True` eller `False` ska vara tillåtet.

De här felen är alltså medvetet inlagda testfel.

### Validering med Pandas

I Pandas skriver jag varje kontroll separat.

Jag använder bland annat:

- `duplicated()` för att hitta dubbletter,
- `between()` för att kontrollera åldersintervallet,
- `isna()` för att hitta saknade värden,
- `isin()` för att kontrollera tillåtna städer,
- och en kontroll av datatyp för `active`.

Om Pandas hittar ett fel läggs ett felmeddelande i en lista som sedan skrivs ut.

### Validering med Pandera

I Pandera samlar jag reglerna i ett schema.

Jag använder `DataFrameSchema`, där varje kolumn får regler. Till exempel ska `customer_id` vara unikt, `age` ska ligga mellan 18 och 100 och `income` får inte saknas.

Jag använder också `lazy=True`. Det gör att Pandera kan samla flera valideringsfel i samma körning i stället för att avsluta direkt vid det första felet.

### Resultat och jämförelse

Både Pandas och Pandera kan upptäcka problemen i testdatan.

Skillnaden är framför allt hur reglerna organiseras.

Med Pandas behöver jag själv skriva varje kontroll och bestämma hur fel ska sparas och visas.

Med Pandera kan jag samla reglerna i ett schema och sedan kontrollera hela DataFrame-objektet mot det schemat.

För ett litet projekt kan Pandas vara fullt tillräckligt. Pandera blir tydligt när man vill samla och återanvända regler för hur data ska se ut.

### Begränsning och vad jag lärde mig

Projektet använder syntetisk data och testar bara några vanliga regler. Jag har inte testat prestanda på stora datamängder eller byggt ett komplett produktionssystem.

Det viktigaste jag lärde mig var hur ett Pandera-schema fungerar och hur det skiljer sig från att skriva separata kontroller i Pandas.

Om jag fortsatte projektet skulle jag vilja testa samma validering på ett större verkligt dataset.


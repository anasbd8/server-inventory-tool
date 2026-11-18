# Redogörelse – Server Inventory Tool

## 1. Tre konstruktioner i Python

### 1a. Villkor

I `checks.py`, i funktionen `check_server()`, innehåller variabeln `is_up` värdet True eller False som kommer från anropet till `ping_server()`. Det är funktionen `ping_server()` som pingar serverns adress. Om `is_up` är True körs raden som sätter serverns status till `"up"`. Annars körs else-grenen och statusen blir `"down"`. Kolon efter if och else visar att ett kodblock börjar, och indragen visar vilka rader som hör till varje gren. Villkoret behövs för att servern ska få rätt status efter kontrollen.

### 1b. Loop

I `menu.py`, i funktionen `run_menu()`, använder jag `while True:` för att visa menyn flera gånger. True gör att loopen fortsätter tills den stoppas. Raderna med indrag under while tillhör loopen och körs igen efter en åtgärd eller ett ogiltigt menyval. När användaren väljer `"0"` körs break, som avslutar loopen. Det gör att användaren kan göra flera saker utan att starta programmet igen.

### 1c. Funktion med parameter och returvärde

I `checks.py` skapas funktionen `ping_server(address)` med def, och parametern address tar emot serverns adress. Funktionen använder `subprocess.run()` för att skicka ett pingpaket och vänta på resultatet, med en tidsgräns på fem sekunder. `return result.returncode == 0` jämför pingprogrammets exitkod med noll och returnerar ett booleskt värde, True eller False. Om processen tar för lång tid fångas TimeoutExpired och funktionen returnerar False. Return avslutar funktionen och skickar tillbaka värdet. I `check_server()` sparas svaret i `is_up`, som sedan används för att uppdatera statusen.

## 2. Datastruktur och datatyper

I `storage.py`, i `load_servers()`, läses serverdatan in till en lista med dictionaries. Listan innehåller alla servrar, och varje dictionary innehåller information om en server. Det passar programmet eftersom det går att gå igenom listan med en loop och läsa ett visst värde genom dess nyckel, till exempel `server["name"]`. I `menu.py`, i `add_server()`, skapas en ny serverpost som läggs till i listan med append.

Varje server har sex nycklar: name, address, environment, role, status och last_checked. Nycklarna och deras värden är strängar. En IP-adress lagras alltså som text, inte som ett tal. Även last_checked är text i ett bestämt datum- och tidsformat, eller en tom sträng om servern inte har kontrollerats. Hela samlingen är en list och varje serverpost är en dict.

## 3. JSON och CSV

Jag använder JSON för att serverdatan ska finnas kvar när programmet avslutas. I `storage.py`, i `load_servers()`, läser `json.load()` filen till Python-objekt. I `save_servers()` skriver `json.dump()` tillbaka listan till filen. JSON passar eftersom det kan lagra både listan och de namngivna fälten i varje server. När något ändras sparas listan så att ändringen finns kvar vid nästa start.

CSV används för rapporten eftersom formatet passar tabeller med kolumner och rader. I `storage.py`, i `export_servers()`, bestämmer fieldnames kolumnernas namn och ordning. `csv.DictWriter` kopplar serverns nycklar till kolumnerna, `writeheader()` skriver rubrikerna och `writerows(servers)` skriver serverraderna. CSV-filen går att öppna i ett kalkylprogram, men det är fortfarande JSON-filen som programmet läser när det startar.

## 4. Moduler och funktioner

Jag har delat upp programmet i fyra Python-filer med olika uppgifter:

- I `main.py` är `main()` startpunkten. Den läser CLI-argumenten och datafilen och väljer vilken åtgärd som ska köras. Om inget åtgärdsargument finns startar den textmenyn. Startvillkoret `if __name__ == "__main__":` gör att main körs när filen startas direkt.
- I `menu.py` sköter `run_menu()` menyn och användarens val. Andra funktioner, som `add_server()` och `remove_server()`, sköter inmatningen för att lägga till och ta bort servrar.
- I `storage.py` läser `load_servers()` JSON, `save_servers()` sparar ändringar och `export_servers()` skapar CSV-rapporten.
- I `checks.py` kör `ping_server()` själva pingkommandot. `check_server()` uppdaterar status och tid och sparar resultatet. `check_all_servers()` går igenom listan och använder samma kontrollfunktion för varje server.

Både `main.main()` och menyfunktionerna anropar de gemensamma kontroll- och lagringsfunktionerna. Både menyn och kommandoraden använder `export_servers()` i storage.py för att skapa CSV-filen. Därför behöver exportkoden bara finnas på ett ställe. Om jag vill ändra exporten ändrar jag den funktionen, och ändringen gäller för båda sätten att köra programmet.

## 5. Standardbiblioteket

Jag använder följande moduler från Pythons standardbibliotek:

- `argparse` används i `main.py`, i `main()`, för att läsa argument som --list och --check. Den visar också hjälptext med --help och kontrollerar de tillåtna miljöerna genom choices.
- `os` används i `main.py`, i `main()`. `os.getenv()` hämtar INVENTORY_DATAFILE, och om variabeln saknas används servers.json.
- `sys` används i `main.py`, i `main()`. `sys.exit()` avslutar kontroll- och exportgrenarna med en exitkod. Vid serverkontroller betyder noll att alla kontrollerade servrar svarade, medan ett betyder att någon är nere eller att det angivna namnet inte finns.
- `pathlib` används bland annat i `storage.py`, i `load_servers()` och `export_servers()`. Path gör det möjligt att hantera sökvägar, kontrollera om datafilen finns och skapa rapportkatalogen om den saknas.
- `json` används i `storage.py`, i `load_servers()` och `save_servers()`, för att läsa och skriva serverlistan.
- `csv` används i `storage.py`, i `export_servers()`, för att skriva rapportens rubriker och serverrader.
- `datetime` används i `checks.py`, i `check_server()`, för tidpunkten för kontrollen. I `storage.py`, i `export_servers()`, används den för tiden i rapportens filnamn. strftime omvandlar tiden till text i valt format.
- `subprocess` används i `checks.py`, i `ping_server()`, för att köra pingkommandot och läsa dess exitkod. Modulen hör till Python, men ping är ett separat program som måste finnas på datorn.

## 6. Tre exempel på god praxis

### Exempel 1. Återanvända samma funktion

I `checks.py` använder `check_all_servers()` funktionen `check_server()` för varje server. Samma check_server används också från `main.main()` och `menu.check_server_by_name()`. Det är bra eftersom kontrollen bara behöver vara skriven på ett ställe. Om sättet att uppdatera status eller spara resultat ändras går det att ändra i den gemensamma funktionen.

### Exempel 2. Stänga filer med with

I `storage.py`, i `load_servers()`, `save_servers()` och `export_servers()`, öppnas filer med with. Det gör att filen stängs automatiskt när programmet lämnar blocket, även om ett fel uppstår inne i det. Jag behöver därför inte lägga till en separat close-rad och riskera att glömma den. Det handlar om att stänga filen korrekt, inte om att alla filfel redan är hanterade.

### Exempel 3. Kontrollera inmatning innan den sparas

I `menu.py`, i `add_server()`, kontrolleras om servernamnet redan finns och om miljön är giltig. Namnen jämförs med casefold så att stora och små bokstäver inte skapar dubbletter. Om miljön är fel frågar programmet igen tills användaren anger dev, test eller prod. Det är bra eftersom felaktiga miljövärden annars skulle försvåra filtreringen, och dubbla namn skulle göra det otydligt vilken server som ska kontrolleras eller tas bort.

## 7. Källor och hjälpmedel

Jag har använt originaluppgiften för att kontrollera vilka funktioner programmet ska ha och för att jämföra startdatan. Ett exempel är serverposterna som läses i `storage.py`, i `load_servers()`. Jag har också använt Codex för förklaringar, kodförslag, felsökning, hjälp att skriva delar av koden och tester. Det gäller bland annat `checks.py`, i `ping_server()` och `check_server()`, och CLI-grenarna i `main.py`, i `main()`. Jag har även fått hjälp att förbättra mina förklaringar och redogörelsen.

Jag tog en del hjälp av Codex för att få `argparse`, `os`, `pathlib` och `subprocess` att fungera. Det gällde argumenten och miljövariabeln i `main.py`, i `main()`, sökvägarna i `storage.py`, i `load_servers()` och `export_servers()`, och pingkommandot i `checks.py`, i `ping_server()`.

Under arbetet har jag bett om stegvisa instruktioner på de delar jag var osäker på, skrivit kod och provkört funktioner. Jag har bland annat provat listning, filtrering, kontroller, export och exitkoder och rapporterat resultaten. Codex har också gjort automatiska kontroller med tillfälliga datafiler och simulerade pingsvar. De testerna kontrollerade bland annat status och sparande i `checks.check_server()` och CSV-innehållet från `storage.export_servers()`. Det skiljer sig från att själv kontrollera riktiga pingsvar i terminalen.

Originaluppgiften: [Server Inventory Tool](https://gist.github.com/jonasbjork/b402dfb3db4b2c63d3e0333fecce3212#file-inlamning-python-md).

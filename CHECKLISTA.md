# Checklista – Server Inventory Tool

För G krävs samtliga G1–G20. För VG krävs dessutom VG1–VG4. Checklistan sammanfattar uppgiften; källan är den fullständiga kravspecifikationen. Klasser och grafiskt gränssnitt ingår inte i kraven.

## Nuläge och viktiga skillnader

Bedömningen bygger på läsning av [main.py](./main.py) och [servers.json](./servers.json), inte på funktionstester. Kryss i denna del betyder att kod finns; kravlistan nedan bockas av efter verifiering.

- [x] Läsa JSON till en lista vid start.
- [x] Använda en tom lista om datafilen saknas.
- [x] Läsa datafilens sökväg från en miljövariabel, med standardvärde.
- [x] Skriva ut namn, miljö och status i vänsterjusterade kolumner.

Kod, nycklar, filnamn och CLI-argument skrivs på engelska. Det avviker medvetet från uppgiftens svenska namn enligt tabellen nedan.

| Namn i koden | Namn i uppgiften |
| --- | --- |
| `INVENTORY_DATAFILE` | `INVENTORY_DATAFIL` |
| `servers.json` | `servrar.json` |
| `name` | `namn` |
| `address` | `adress` |
| `environment` | `miljo` |
| `role` | `roll` |
| `status` | `status` |
| `last_checked` | `senast_kontrollerad` |
| `webserver` | `webbserver` |
| `database` | `databas` |
| `testserver` | `testserver` |
| `developmentserver` | `utvecklingsserver` |
| `reports/` | `rapporter/` |
| `inventory_2026-11-03_1337.csv` | `inventering_2026-11-03_1337.csv` |
| `--list` | `--lista` |
| `--environment` | `--miljo` |
| `--check` | `--kontrollera` |
| `--check-all` | `--kontrollera-alla` |
| `--export` | `--export` |

## G: data och validering

- [ ] **G1:** Håll servrarna i en lista med dictionaries med samtliga sex nycklar: `name`, `address`, `environment`, `role`, `status` och `last_checked`. Programmet ska fungera med uppgiftens startdata, översatt till dessa namn.
- [ ] **G2:** Tillåt miljöerna `dev`, `test`, `prod` och statusvärdena `up`, `down`, `unknown`. Nya servrar ska alltid få `unknown`.
- [ ] **G3:** Kontrollera miljön när en server läggs till. Visa ett meddelande och fråga igen tills värdet är giltigt.
- [ ] **G4:** Förhindra att två servrar läggs till med samma namn.

## G: lagring och export

- [ ] **G5:** Läs JSON vid start och spara till samma fil efter varje ändring, även efter kontroller.
- [ ] **G6:** Läs sökvägen från `INVENTORY_DATAFILE`, annars använd `servers.json`.
- [ ] **G7:** Kontrollera filens existens med `Path.exists()` och starta med en tom lista om filen saknas.
- [ ] **G8:** Exportera alla servrar till CSV med rubrikrad. Skapa `reports/` automatiskt och använd datum och tid i filnamnet, exempelvis `inventory_2026-11-03_1337.csv`.

## G: serverkontroller

- [ ] **G9:** Kör ping med `subprocess.run()`, skicka kommandot som en lista och avgör resultatet från exitkoden.
- [ ] **G10:** Sätt `status` till `up` eller `down`, sätt `last_checked` till aktuell tid i formatet `ÅÅÅÅ-MM-DD TT:MM` och spara ändringen till JSON.

Pingflaggorna behöver passa körmiljön. Uppgiften utgår från Linux/macOS; på Windows kan WSL eller kursens miljö användas. Ett uteblivet pingsvar från internet kan bero på nätverket och ska ge `down`.

## G: textmeny

- [ ] **G11:** Start utan argument visar en meny som upprepas tills användaren avslutar.
  - [ ] Visa alla servrar.
  - [ ] Visa servrar i vald miljö.
  - [ ] Lägg till en server.
  - [ ] Ta bort en server.
  - [ ] Kontrollera en server.
  - [ ] Kontrollera alla servrar.
  - [ ] Exportera CSV.
  - [ ] Avsluta.
- [ ] **G12:** Hantera ogiltiga menyval med ett begripligt meddelande och visa menyn igen. Meddela om ett angivet servernamn inte finns.
- [ ] **G13:** Begär extra bekräftelse innan en server i `prod` tas bort.
- [ ] **G14:** Visa servrar i läsbara, linjerade kolumner med f-strängar och fältbredder.

## G: kommandorad

- [ ] **G15:** Använd `argparse` i startpunkten och stöd alla anrop nedan.

| Anrop | Förväntat beteende |
| --- | --- |
| `python main.py` | Starta textmenyn. |
| `python main.py --help` | Visa hjälptext. |
| `python main.py --list` | Lista alla servrar och avsluta. |
| `python main.py --list --environment prod` | Visa endast produktionsservrar. |
| `python main.py --check web01` | Kontrollera den namngivna servern. |
| `python main.py --check-all` | Kontrollera alla servrar. |
| `python main.py --export` | Skapa CSV-rapport. |

Använd `python3` i stället för `python` om det är interpreterkommandot i din miljö.

- [ ] **G16:** Använd `sys.exit()` för rätt exitkoder.
  - [ ] `0` när körningen lyckas.
  - [ ] `1` efter kontroll om minst en kontrollerad server är nere.
  - [ ] `1` om servern i `--check` inte finns.

## G: struktur och dokumentation

- [ ] **G17:** Dela upp programmet i minst tre egna moduler med tydliga ansvar. Behåll [main.py](./main.py) som startpunkt och använd `if __name__ == "__main__":`.
- [ ] **G18:** Följ kodriktlinjerna.
  - [ ] Beskrivande variabel- och funktionsnamn på engelska i `snake_case`.
  - [ ] Funktioner har en tydlig uppgift och tar emot sina beroenden som parametrar.
  - [ ] Kommentera sådant som inte framgår av koden.
  - [ ] Återanvänd samma lagrings- och kontrollfunktioner från meny och CLI.
  - [ ] Undvik duplicerad logik och hemligheter i koden.
  - [ ] Skapa `.gitignore` med minst `__pycache__/` och `reports/`.
- [ ] **G19:** Skriv en omfattande `README.md` som beskriver syfte, körkrav, meny, CLI-exempel, miljövariabel och projektstruktur.
- [ ] **G20:** Skriv `REDOGORELSE.md` med egna ord och konkreta hänvisningar till fil och funktion i varje svar.
  - [ ] Förklara syntax och funktion för tre olika konstruktioner, exempelvis villkor, loop och funktion med parametrar och `return`.
  - [ ] Motivera listan med dictionaries och beskriv servervärdenas datatyper.
  - [ ] Motivera JSON för lagring och CSV för rapporter.
  - [ ] Förklara modulindelningen och varje fils ansvar.
  - [ ] Beskriv använda standardbiblioteksmoduler och deras användning.
  - [ ] Ge och motivera tre exempel på god praxis från koden.
  - [ ] Redovisa källor och hjälpmedel, inklusive eventuell AI, och vad de användes till.

### Föreslagen ansvarsfördelning (inte låsta filnamn)

| Fil | Ansvar |
| --- | --- |
| [main.py](./main.py) | Startpunkt, argumenttolkning och exitkoder. |
| `menu.py` | Menyloop och användarinteraktion. |
| `storage.py` | JSON-inläsning, sparande och CSV-export. |
| `checks.py` | Ping och uppdatering av kontrollresultat. |

Uppgiften tillåter andra filnamn om ansvar och motivering framgår i dokumentationen.

## VG: fördjupningar och reflektion

- [ ] **VG1:** Välj och genomför minst två fördjupningar. Beskriv varje vald fördjupning i `README.md` och motivera den i `REFLEKTION.md`.

Markera endast de alternativ som du väljer och slutför; alla sex krävs inte.

- [ ] **HTTP-kontroll:** Kontrollera även HTTP för rollen `webserver` genom `curl` via `subprocess.run()`. Välj flaggor som ger användbar exitkod och begränsad väntetid.
- [ ] **Historik:** Spara tid och resultat per kontroll och server. Visa senaste kontroller både i menyn och via ett eget CLI-argument.
- [ ] **Sammanfattande rapport:** Komplettera CSV med en textrapport med antal `up`, `down`, `unknown`, totalt och per miljö.
- [ ] **Konfigurationsfil:** Läs datafil och rapportkatalog från `config.json`. Prioritera miljövariabel före konfigurationsfil före standardvärde och dokumentera ordningen.
- [ ] **Säkrare inmatning:** Fråga igen vid tomma fält, namn med mellanslag och ogiltiga menyval. Undersök lämpliga strängmetoder.
- [ ] **Verbose:** Lägg till `--verbose` med extra information, exempelvis körda kommandon och använd datafil.

En egen fördjupning med motsvarande omfattning behöver stämmas av med läraren innan arbetet påbörjas.

- [ ] **VG2:** Värdera minst fyra egna val i `REFLEKTION.md`. Beskriv för varje val alternativ, motivering, för- och nackdelar samt vad ändrade förutsättningar skulle innebära.
  - [ ] Minst två val kommer från uppgiftens lista: datastruktur, spara efter varje ändring, modulindelning, miljövariabel, `subprocess` och externa kommandon, kommando som lista eller meny tillsammans med CLI.
- [ ] **VG3:** Resonera om förändringar för exempelvis 1 000 servrar eller nattlig automatisk körning i en pipeline.
- [ ] **VG4:** Skriv med egna ord, hänvisa till konkreta kodställen och värdera varför lösningarna är lämpliga. Riktmärke: två till tre sidor.

## Rekommenderad arbetsordning

Detta är ett arbetsförslag, inte ytterligare betygskrav.

1. Kontrollera att `servers.json` motsvarar uppgiftens startdata, med engelska namn.
2. Dela upp ansvar och skapa gemensamma funktioner för läsning och sparande.
3. Implementera serverhantering, validering och textmeny.
4. Implementera ping, tidsstämplar och sparande av kontrollresultat.
5. Implementera CSV-export.
6. Koppla CLI-argument till samma funktioner som menyn och sätt exitkoder.
7. Verifiera G-kraven och skriv dokumentationen.
8. Genomför minst två fördjupningar och reflektionen om du siktar på VG.

## Slutkontroll och inlämning

- [ ] Prova samtliga menyval och CLI-anrop ovan.
- [ ] Kontrollera ogiltig miljö, dubblerat namn, okänd server och ogiltigt menyval.
- [ ] Kontrollera att nekad bekräftelse behåller en produktionsserver och godkänd bekräftelse tar bort den.
- [ ] Starta om efter tillägg, borttagning och ping; kontrollera att ändringarna finns kvar.
- [ ] Prova både saknad datafil och en alternativ datafil via `INVENTORY_DATAFILE`.
- [ ] Kontrollera CSV-rubriker, innehåll, katalog och tidsstämpel i filnamnet.
- [ ] Kontrollera exitkoder direkt efter körning, exempelvis med `echo $?` i Bash.
- [ ] Kontrollera start från en ny klon genom att följa README-instruktionerna.
- [ ] Säkerställ att Git-repot innehåller kod, startdata, `.gitignore`, `README.md` och `REDOGORELSE.md`, samt `REFLEKTION.md` för VG.
- [ ] Lämna inte med `__pycache__/` eller genererade rapporter.
- [ ] Säkerställ att läraren kan läsa repot: publikt eller med `jonasbjork` som collaborator.
- [ ] Lämna in länken till Git-repot på LearnPoing enligt uppgiften.

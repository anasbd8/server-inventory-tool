# Server Inventory Tool

Ett kommandoradsprogram i Python för att hålla ordning på servrar: namn, adress, miljö, roll, status och senaste kontroll.

> **Status:** Programmet kan i dag bara läsa datafilen och visa servrarna i en tabell. Meny, kontroller, CSV-export och CLI-argument är planerade men inte byggda. Se [CHECKLISTA.md](./CHECKLISTA.md).

## Körkrav

- Python 3.
- Inga externa paket. Programmet använder bara standardbiblioteket.

## Köra programmet

Kör från projektkatalogen, eftersom standardsökvägen till datafilen är relativ till den katalog du står i:

```bash
python3 main.py
```

Programmet skriver ut alla servrar i kolumner:

```text
Name           Environment    Status
web01          prod           unknown
db01           prod           unknown
test01         test           unknown
dev01          dev            unknown
```

## Miljövariabel

`INVENTORY_DATAFILE` anger vilken datafil som ska läsas. Utan variabeln används `servers.json`.

```bash
INVENTORY_DATAFILE=annan_fil.json python3 main.py
```

Om filen saknas startar programmet med en tom lista och visar bara rubrikraden.

## Datafil

`servers.json` innehåller en lista med servrar. Varje server har sex nycklar:

| Nyckel | Innehåll | Exempel |
| --- | --- | --- |
| `name` | Serverns namn | `web01` |
| `address` | Värdnamn eller IP-adress | `example.com` |
| `environment` | Miljö: `dev`, `test` eller `prod` | `prod` |
| `role` | Serverns roll | `webserver` |
| `status` | Status: `up`, `down` eller `unknown` | `unknown` |
| `last_checked` | Tid för senaste kontroll, tom om servern inte har kontrollerats | `""` |

## Projektstruktur

| Fil | Ansvar |
| --- | --- |
| `main.py` | Läser datafilen och visar servrarna. |
| `servers.json` | Startdata. |
| `CHECKLISTA.md` | Uppgiftens krav och vad som återstår. |
| `REDOGORELSE.md` | Redogörelse för G-kraven. |
| `REFLEKTION.md` | Reflektion för VG-kraven. |

## Planerat, inte byggt

Följande anrop fungerar **inte** ännu. Argumenten läses inte, så alla anrop visar i dag bara tabellen.

| Anrop | Tänkt beteende |
| --- | --- |
| `python3 main.py --list` | Lista alla servrar och avsluta. |
| `python3 main.py --list --environment prod` | Visa endast produktionsservrar. |
| `python3 main.py --check web01` | Kontrollera den namngivna servern. |
| `python3 main.py --check-all` | Kontrollera alla servrar. |
| `python3 main.py --export` | Skapa CSV-rapport i `reports/`. |

Start utan argument ska visa en textmeny med val för att visa, lägga till, ta bort och kontrollera servrar, exportera CSV och avsluta.

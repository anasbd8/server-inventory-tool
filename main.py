"""Läser in och visar en enkel inventering av servrar.

Programmet försöker läsa serverinformationen från filen ``servers.json``.
Om filen inte finns används en tom lista, så att programmet fortfarande kan
starta utan att krascha.
"""

import os # Används för att läsa miljövariabler, om det behövs.
from pathlib import Path  # Ger ett plattformsoberoende sätt att hantera filsökvägar.
from storage import load_servers  # Importerar funktioner för att läsa och skriva JSON-data.

# Sökvägen till JSON-filen som innehåller serverinformationen.
# Sökvägen är relativ till den katalog där programmet körs.
data_file = Path(os.getenv("INVENTORY_DATAFILE", "servers.json"))

servers = load_servers(data_file)


def display_servers(servers):
    """Skriver ut alla servrar i ett tabelliknande format.

    Parametrar:
        servers: En lista med ordböcker. Varje ordbok måste innehålla nycklarna
            ``name``, ``environment`` och ``status``.

    Returvärde:
        Funktionen returnerar inget värde. Den skriver informationen direkt
        till terminalen med ``print``.
    """

    # Skriv ut tabellens rubriker.
    # ``<15`` och ``<10`` betyder vänsterjustering i ett fält med angiven bredd.
    print(f"{'Name':<15}{'Environment':<15}{'Status':<10}")

    # Gå igenom varje server i listan en i taget.
    for server in servers:
        # Läs serverns tre fält och skriv ut dem med samma kolumnbredder
        # som rubrikerna ovan.
        print(f"{server['name']:<15}{server['environment']:<15}{server['status']:<10}")


# Kör funktionen med serverlistan som lästes in från JSON-filen.
display_servers(servers)

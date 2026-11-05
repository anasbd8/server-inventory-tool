import json

def load_servers(data_file):
    # Kontrollera om JSON-filen finns innan vi försöker öppna den.
    if data_file.exists():
        # Öppna filen i läsläge ("r" = read) och stäng den automatiskt
        # när blocket är färdigt tack vare ``with``.
        with open(data_file, "r") as file:
            # Konvertera JSON-innehållet till Python-objekt.
            # Här förväntas innehållet vara en lista med server-ordböcker, till exempel:
            # [{"name": "web-01", "environment": "Production", "status": "Online"}]
            servers = json.load(file)
    else:
        # Om filen saknas finns det inga servrar att visa.
        # En tom lista gör att programmet kan fortsätta utan fel.
        servers = []
        # Returnera [] om filen saknas.
    return servers

def save_servers(servers, data_file):
    # Spara serverlistan som JSON.
    with open(data_file, "w") as file:
        json.dump(servers, file)
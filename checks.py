"""Funktioner för att kontrollera om servrar svarar på ping."""

# subprocess låter Python köra externa program, till exempel ping.
import subprocess
from datetime import datetime

from storage import save_servers


def ping_server(address):
    """Returnera True om adressen svarar, annars False (Linux/macOS).

    Om ping inte kan startas får anroparen hantera felet.
    """
    try:
        # Skicka kommandot som en lista: -c 1 betyder ett pingpaket.
        # capture_output fångar utskriften så att den inte stör menyn.
        # timeout avbryter processen om den tar mer än fem sekunder.
        result = subprocess.run(
            ["ping", "-c", "1", address],
            capture_output=True,
            timeout=5,
        )
    except subprocess.TimeoutExpired:
        # Ett uteblivet svar inom tidsgränsen räknas som nere.
        return False

    # Exitkod 0 betyder att ping lyckades. Övriga koder ger False.
    return result.returncode == 0


def check_server(server, servers, data_file):
    """Kontrollera en server, spara hela listan och returnera om den svarade."""
    # Kör ping innan vi ändrar servern. Om ping inte kan startas behålls datan.
    is_up = ping_server(server["address"])

    # Uppdatera samma dictionary som finns i serverlistan.
    if is_up:
        server["status"] = "up"
    else:
        server["status"] = "down"

    # Spara lokal tid som text, exempelvis 2026-11-10 21:30.
    server["last_checked"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Spara hela listan så att resultatet finns kvar efter en omstart.
    save_servers(servers, data_file)
    return is_up

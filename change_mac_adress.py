import subprocess

# Definizione delle variabili
interfaccia = "eth0"  # Nome dell'interfaccia di rete da modificare
nuovo_mac = "2a:1b:22:3c:4d:ef"  # Nuovo indirizzo MAC da assegnare


def cambio_mac(interfaccia, nuovo_mac):
    # Spegnimento della scheda di rete
    print("Script in esecuzione, spegnimento scheda di rete")
    subprocess.run(["ip", "link", "set", interfaccia, "down"])
    # Cambio dell'indirizzo MAC
    print(
        f"Cambiamento dell'indirizzo MAC dell'interfaccia {interfaccia} a {nuovo_mac}"
    )
    subprocess.run(["ip", "link", "set", interfaccia, "address", nuovo_mac])
    # Conferma del cambio dell'indirizzo MAC
    print(f"Indirizzo MAC cambiato a {nuovo_mac}")
    # Riattivazione della scheda di rete
    subprocess.run(["ip", "link", "set", interfaccia, "up"])
    print("Scheda di rete riattivata")


if __name__ == "__main__":
    cambio_mac(interfaccia, nuovo_mac)

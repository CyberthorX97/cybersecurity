import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import getpass

def genera_chiave(password, salt):
    # Deriva una chiave dalla password usando PBKDF2
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    chiave = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return chiave

def cifra_file(percorso_file, chiave):
    fernet = Fernet(chiave)
    with open(percorso_file, 'rb') as file:
        dati = file.read()
    dati_cifrati = fernet.encrypt(dati)
    with open(percorso_file, 'wb') as file:
        file.write(dati_cifrati)

def decifra_file(percorso_file, chiave):
    fernet = Fernet(chiave)
    with open(percorso_file, 'rb') as file:
        dati_cifrati = file.read()
    dati_decifrati = fernet.decrypt(dati_cifrati)
    with open(percorso_file, 'wb') as file:
        file.write(dati_decifrati)

def cifra_cartella(percorso_cartella):
    # Chiedi la password all'utente
    password = getpass.getpass("Inserisci la password per la cifratura: ")
    
    # Genera un salt casuale
    salt = os.urandom(16)
    
    # Genera la chiave
    chiave = genera_chiave(password, salt)
    
    # Cifra ogni file
    for root, dirs, files in os.walk(percorso_cartella):
        for file in files:
            percorso_file = os.path.join(root, file)
            cifra_file(percorso_file, chiave)
    
    # Salva il salt
    with open(os.path.join(percorso_cartella, 'salt.salt'), 'wb') as salt_file:
        salt_file.write(salt)
    
    print("Cartella cifrata con successo!")

def decifra_cartella(percorso_cartella):
    # Leggi il salt
    try:
        with open(os.path.join(percorso_cartella, 'salt.salt'), 'rb') as salt_file:
            salt = salt_file.read()
    except FileNotFoundError:
        print("File salt non trovato. Impossibile decifrare.")
        return
    
    # Chiedi la password all'utente
    password = getpass.getpass("Inserisci la password per la decifratura: ")
    
    # Genera la chiave
    chiave = genera_chiave(password, salt)
    
    # Prova a decifrare i file
    for root, dirs, files in os.walk(percorso_cartella):
        for file in files:
            if file != 'salt.salt':
                percorso_file = os.path.join(root, file)
                try:
                    decifra_file(percorso_file, chiave)
                except Exception as e:
                    print(f"Password errata o file corrotto. Decifratura fallita: {e}") 
                    return  # Esce immediatamente se la password è sbagliata
    
    # Se tutto va bene, rimuovi il salt
    os.remove(os.path.join(percorso_cartella, 'salt.salt'))
    print("Cartella decifrata con successo!")

# Esempio di utilizzo
if __name__ == "__main__":
    cartella = "INSERIRE PERCORSO CARTELLA"  # Sostituisci con il tuo percorso
    
    azione = input("Vuoi cifrare o decifrare la cartella? (cifrare/decifrare): ").lower()
    if azione == "cifrare":
        cifra_cartella(cartella)
    elif azione == "decifrare":
        decifra_cartella(cartella)
    else:
        print("Scelta non valida. Usa 'cifrare' o 'decifrare'.")
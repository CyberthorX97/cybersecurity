import os
from cryptography.hazmat.primitives import serialization, hashes, padding as sym_padding
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

### 🔐 CONFIGURAZIONE ###
TEST_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "RANSOMWARE_SIMULATION_TEST")
PRIVATE_KEY_FILE = "private_key.pem"  # Chiave privata generata durante la cifratura
ENCRYPTED_AES_KEY_FILE = "encrypted_aes_key.bin"  # Chiave AES cifrata

### 🔓 FUNZIONE PRINCIPALE ###
def decifra_tutti_file():
    """Decifra tutti i file nella cartella di test usando la chiave privata RSA."""
    # Carica la chiave privata RSA
    try:
        with open(os.path.join(TEST_DIR, PRIVATE_KEY_FILE), "rb") as f:
            chiave_privata = serialization.load_pem_private_key(
                f.read(),
                password=None,
                backend=default_backend()
            )
    except Exception as e:
        print(f"❌ Errore caricamento chiave privata: {e}")
        return

    # Decifra la chiave AES
    try:
        with open(os.path.join(TEST_DIR, ENCRYPTED_AES_KEY_FILE), "rb") as f:
            chiave_aes_cifrata = f.read()
        
        chiave_aes = chiave_privata.decrypt(
            chiave_aes_cifrata,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except Exception as e:
        print(f"❌ Errore decifratura chiave AES: {e}")
        return

    # Cerca tutti i file cifrati (.encrypted)
    for root, _, files in os.walk(TEST_DIR):
        for file in files:
            if file.endswith(".encrypted"):
                file_path = os.path.join(root, file)
                output_path = file_path[:-10]  # Rimuove ".encrypted"
                print(f"🔓 Decifrando {file_path}...")
                
                try:
                    with open(file_path, "rb") as f:
                        iv = f.read(16)  # Legge l'IV (primi 16 byte)
                        dati_cifrati = f.read()
                    
                    # Configura AES-CBC
                    cipher = Cipher(
                        algorithms.AES(chiave_aes),
                        modes.CBC(iv),
                        backend=default_backend()
                    )
                    decryptor = cipher.decryptor()
                    
                    # Decifra e rimuove il padding
                    dati_decifrati = decryptor.update(dati_cifrati) + decryptor.finalize()
                    unpadder = sym_padding.PKCS7(128).unpadder()
                    dati_originali = unpadder.update(dati_decifrati) + unpadder.finalize()
                    
                    # Salva il file originale
                    with open(output_path, "wb") as f:
                        f.write(dati_originali)
                    
                    # Elimina il file cifrato
                    os.remove(file_path)
                    print(f"✅ File decifrato salvato come: {output_path}")
                
                except Exception as e:
                    print(f"❌ Errore decifratura {file_path}: {e}")

if __name__ == "__main__":
    print("=== DECRIPTATORE SIMULAZIONE RANSOMWARE ===")
    print("⚠️ USO DIDATTICO - NON PER ATTACCHI REALI ⚠️\n")
    
    if not os.path.exists(TEST_DIR):
        print(f"❌ Cartella {TEST_DIR} non trovata!")
    else:
        decifra_tutti_file()
        print("\n🎉 Decifratura completata!")
